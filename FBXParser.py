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
'''
def display(node, indent):
    if not node: return

    print("%s%s" % (indent, node.GetNodeAttribute()))
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()

        if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
            print(child)
            
        display(child, indent + "  ")
'''
def generate_svg(fbx_path):
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()

    if not FbxCommon.LoadScene(sdk_manager, scene, fbx_path):
        print("Error in LoadScene")
    
    node = scene.GetRootNode()

    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        mesh = child.GetMesh()

        edges = get_edges(mesh)
        edges = get_control_points(mesh, edges)

    svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    svg_content += "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"360\">\n"
    svg_content += "<g fill=\"none\" stroke=\"#000\" stroke-width=\"3\">\n"
    svg_content += generate_svg_path(edges) + "\n"
    svg_content += "</g>\n" + "</svg>"
    print(svg_content)

    svg_file = open("box_wire.svg", "w")
    svg_file.write(svg_content)
    svg_file.close()

def get_edges(mesh):
    edges = []
        
    for j in range(mesh.GetMeshEdgeCount()):
        edges.append(mesh.GetMeshEdgeVertices(j))

    return edges

def get_control_points(mesh, edge_array):
    control_points = []

    for i in range(len(edge_array)):
        temp = []

        for j in range(len(edge_array[i])):
            temp.append(mesh.GetControlPointAt(edge_array[i][j]))

        control_points.append(temp)

    return control_points

def generate_svg_path(edge_array):
    svg_path = "<path d=\""

    for i in range(len(edge_array)):
        temp = "M" + str(edge_array[i][0][0]) + "," + str(edge_array[i][0][1]) + " "
        temp += "L" + str(edge_array[i][1][0]) + "," + str(edge_array[i][1][1]) + " "

        svg_path += temp

    svg_path += "\"/>"
    return svg_path

generate_svg("cube.fbx")
