# code reduced from https://wiki.python.org/moin/BaseHttpServer
import time
import BaseHTTPServer
import FbxCommon

# example of a python class
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(s):
    """Respond to a GET request."""
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><head><title>Title goes here.</title></head>")
    s.wfile.write("<body><p>This is a test.</p>")
    s.wfile.write("<p>You accessed path: %s</p>" % s.path)
    s.wfile.write("</body></html>")


def display(node, indent):
  if not node: return

  print("%s%s" % (indent, node.GetNodeAttribute()))
  for i in range(node.GetChildCount()):
    child = node.GetChild(i)
    attr_type = child.GetNodeAttribute().GetAttributeType()

    if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
      print(child)

    display(child, indent + "  ")

    
sdk_manager, scene = FbxCommon.InitializeSdkObjects()

if not FbxCommon.LoadScene(sdk_manager, scene, "cube.fbx"):
  print("error in LoadScene")

#display(scene.GetRootNode(), "")

httpd = BaseHTTPServer.HTTPServer(("192.168.1.100", 8000), MyHandler)
httpd.serve_forever()
