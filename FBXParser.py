import time
import BaseHTTPServer
import FbxCommon

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>test</p></body>")
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
            #print(child.GetMesh().GetPolygonVertexCount())

        display(child, indent + "  ")

def get_vertices(node):
    if not node: return

    for i in range(node.GetChildCount()):
        print("Break")
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()

        if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
            vertices = child.GetMesh().GetControlPoints()

            for i in range(len(vertices)):
                print(vertices[i])

sdk_manager, scene = FbxCommon.InitializeSdkObjects()

if not FbxCommon.LoadScene(sdk_manager, scene, "cube.fbx"):
    print("Error in LoadScene")

#display(scene.GetRootNode(), "")
get_vertices(scene.GetRootNode())
