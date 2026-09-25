"""Single-operator loopback server. Run: python3 -m rsi.server."""
import argparse
import base64
import hashlib
import re
import hmac
import json
import mimetypes
import os
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from .core import Store, Service, Problem

ROOT=Path(__file__).resolve().parent.parent
MAX_BODY=5_000_000

def make_handler(service,port,token=None):
    token=token or secrets.token_urlsafe(32)
    hosts={f'127.0.0.1:{port}',f'localhost:{port}'}
    class Handler(BaseHTTPRequestHandler):
        server_version='RSICopiloto'
        def log_message(self,fmt,*args):
            # Never log user content, keys or request bodies.
            pass
        def allowed_host(self):
            return self.headers.get('Host','') in hosts
        def respond(self,status,payload,ctype='application/json; charset=utf-8'):
            if isinstance(payload,(dict,list)): payload=json.dumps(payload,ensure_ascii=False).encode()
            if isinstance(payload,str): payload=payload.encode()
            self.send_response(status)
            self.send_header('Content-Type',ctype)
            self.send_header('Content-Length',str(len(payload)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Referrer-Policy','no-referrer')
            hashes=' '.join("'sha256-"+base64.b64encode(hashlib.sha256(x).digest()).decode()+"'" for x in re.findall(rb'<script>(.*?)</script>',payload,re.S)) if ctype.startswith('text/html') else ''
            self.send_header('Content-Security-Policy',f"default-src 'self'; script-src 'self' {hashes}; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(payload)
        def do_GET(self):
            if not self.allowed_host(): return self.respond(403,{'error':'Host não autorizado.'})
            path=urlsplit(self.path).path
            if path=='/api/session':
                return self.respond(200,{'token':token})
            if path.startswith('/api/'):
                if not hmac.compare_digest(self.headers.get('X-RSI-Token',''),token):
                    return self.respond(403,{'error':'Recarregue a página para abrir a sessão local.'})
                if path=='/api/state': return self.respond(200,service.state())
                return self.respond(404,{'error':'Rota não encontrada.'})
            if path=='/': path='/app/index.html'
            if path.endswith('/'): path+='index.html'
            file=(ROOT/unquote(path).lstrip('/')).resolve()
            if not any(file.is_relative_to(ROOT/p) for p in ['app','guia','capa']) or not file.is_file():
                return self.respond(404,'Arquivo não encontrado.','text/plain; charset=utf-8')
            mime=mimetypes.guess_type(file)[0] or 'application/octet-stream'
            return self.respond(200,file.read_bytes(),mime)
        def do_POST(self):
            if not self.allowed_host(): return self.respond(403,{'error':'Host não autorizado.'})
            origin=self.headers.get('Origin')
            if origin and origin not in {f'http://{host}' for host in hosts}:
                return self.respond(403,{'error':'Origem não autorizada.'})
            if not hmac.compare_digest(self.headers.get('X-RSI-Token',''),token):
                return self.respond(403,{'error':'Sessão inválida. Recarregue a página.'})
            if urlsplit(self.path).path!='/api/action': return self.respond(404,{'error':'Rota não encontrada.'})
            if self.headers.get_content_type()!='application/json': return self.respond(415,{'error':'Use JSON.'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=MAX_BODY: raise Problem('Arquivo ou solicitação muito grande.',413)
                data=json.loads(self.rfile.read(size))
                if not isinstance(data,dict) or not isinstance(data.get('data',{}),dict): raise Problem('Solicitação inválida.')
                result=service.action(data.get('action'),data.get('data',{}))
                return self.respond(200,result)
            except Problem as e: return self.respond(e.status,{'error':str(e)})
            except (ValueError,UnicodeError): return self.respond(400,{'error':'JSON inválido.'})
            except Exception:
                return self.respond(500,{'error':'Erro interno. Seus dados persistidos foram preservados; consulte os testes ou reinicie o servidor.'})
    return Handler

def main():
    parser=argparse.ArgumentParser(description='RSI Copiloto — assistente local com IA supervisionada')
    parser.add_argument('--port',type=int,default=8765)
    parser.add_argument('--db',default=os.getenv('RSI_DB',str(Path.home()/'.local/share/rsi-copiloto/state.sqlite3')))
    parser.add_argument('--no-scheduler',action='store_true')
    args=parser.parse_args()
    if not 1024<=args.port<=65535: parser.error('porta deve estar entre 1024 e 65535')
    service=Service(Store(Path(args.db).expanduser()))
    server=ThreadingHTTPServer(('127.0.0.1',args.port),make_handler(service,args.port))
    stop=threading.Event()
    def scheduler():
        while not stop.wait(30):
            try: service.tick()
            except Exception: print('Falha no agendador. Confira o banco e reinicie o servidor.',flush=True)
    if not args.no_scheduler: threading.Thread(target=scheduler,daemon=True).start()
    print(f'RSI Copiloto: http://127.0.0.1:{args.port}/app/ | IA: {"configurada" if service.provider.key else "sem credencial"}',flush=True)
    print('Dados locais; uso individual. Ctrl+C para encerrar.',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: stop.set(); server.server_close()

if __name__=='__main__': main()
