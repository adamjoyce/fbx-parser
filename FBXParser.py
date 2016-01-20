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
        #print(edges)
        edge_control_points = get_control_points(mesh, edges)
        print(edge_control_points)
        print("\n")

        smallest_control_points = get_smallest_control_points(edge_control_points)
        print(smallest_control_points)
        print("\n")

    svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    svg_content += "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"360\">\n"
    svg_content += "<g fill=\"none\" stroke=\"#000\" stroke-width=\"3\">\n"
    svg_content += generate_svg_path(edge_control_points, smallest_control_points) + "\n"
    svg_content += "</g>\n" + "</svg>"
    #print(svg_content)

    svg_file = open("box_wire.svg", "w")
    svg_file.write(svg_content)
    svg_file.close()

def get_edges(mesh):
    edges = []
        
    for j in range(mesh.GetMeshEdgeCount()):
        edges.append(mesh.GetMeshEdgeVertices(j))

    return edges

def get_control_points(mesh, edges):
    control_points = []

    for i in range(len(edges)):
        temp = []

        for j in range(len(edges[i])):
            temp.append(mesh.GetControlPointAt(edges[i][j]))

        control_points.append(temp)
    
    return control_points

def get_smallest_control_points(control_points):
    smallest_control_points = []
    smallest_x = 0.0
    smallest_y = 0.0
    smallest_z = 0.0

    for i in range(len(control_points)):
        for j in range(len(control_points[i])):
            if control_points[i][j][0] < smallest_x:
                smallest_x = control_points[i][j][0]
            if control_points[i][j][1] < smallest_y:
                smallest_y = control_points[i][j][1]
            if control_points[i][j][2] < smallest_z:
                smallest_z = control_points[i][j][2]

    smallest_control_points = [smallest_x, smallest_y, smallest_z]
    return smallest_control_points

def generate_svg_path(control_points, smallest_control_points):
    offset = 100

    svg_path = "<path d=\""

    for i in range(len(control_points)):
        temp = "M" + str(control_points[i][0][0] - smallest_control_points[0] + offset) + "," + str(control_points[i][0][1] - smallest_control_points[1] + offset) + " "
        temp += "L" + str(control_points[i][1][0] - smallest_control_points[0] + offset) + "," + str(control_points[i][1][1] - smallest_control_points[1] + offset) + " "

        svg_path += temp

    svg_path += "\"/>"
    return svg_path

generate_svg("cube.fbx")
