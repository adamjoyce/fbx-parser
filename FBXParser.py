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

    svg_content = write_meta_data()

    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        mesh = child.GetMesh()

        svg_content += write_edges(mesh)
        #svg_content += write_faces(mesh)
        
        control_points = mesh.GetControlPoints()
        smallest_control_points = find_smallest_control_points(control_points)

        svg_content += write_coordinates(control_points, smallest_control_points)
        svg_content += write_centres(smallest_control_points)

        svg_content += write_functions()

        #edges = get_edges(mesh)
        #print(edges)
        #edge_control_points = get_control_points(mesh, edges)
        #print(edge_control_points)
        #print("\n")

        #smallest_control_points = get_smallest_control_points(edge_control_points)
        #print(smallest_control_points)
        #print("\n")

    svg_content += "]]>\n</script>\n"
    svg_content += "</svg>"
    
    svg_file = open("box_wire.svg", "w")
    svg_file.write(svg_content)
    svg_file.close()

def write_meta_data():
    svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    svg_content += "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100%\" height=\"100%\" onload=\"init(evt)\">\n"
    svg_content += "<style>\n.edge{\nfill: white;\nstroke: black;\nstroke-width: 1;\n}\n</style>\n\n"
    svg_content += "<script type=\"text/ecmascript\">\n"
    svg_content += "<![CDATA[\n"
    return svg_content

def write_edges(mesh):
    edges = "edges = ["
    for i in range(mesh.GetMeshEdgeCount()):
        vertices = mesh.GetMeshEdgeVertices(i)
        start_vertex = vertices[0]
        end_vertex = vertices[1]
        edges += "[" + str(start_vertex) + "," + str(end_vertex) + "],"
    edges = edges[:-1] + "]\n"
    return edges

def write_faces(mesh):
    faces = "faces = ["
    #for i in range(mesh.GetPolygonCount()):


def write_coordinates(control_points, smallest_control_points):
    x_coordinates = "x coordinates = ["
    y_coordinates = "y coordinates = ["
    z_coordinates = "z coordinates = ["

    for i in range(len(control_points)):
        x_coordinates += str(control_points[i][0] - smallest_control_points[0]) + ","
        y_coordinates += str(control_points[i][1] - smallest_control_points[1]) + ","
        z_coordinates += str(control_points[i][2] - smallest_control_points[2]) + ","

    x_coordinates = x_coordinates[:-1] + "];\n"
    y_coordinates = y_coordinates[:-1] + "];\n"
    z_coordinates = z_coordinates[:-1] + "];\n\n"

    return x_coordinates + y_coordinates + z_coordinates

def find_smallest_control_points(control_points):
    smallest_x = 0.0
    smallest_y = 0.0
    smallest_z = 0.0
    smallest_control_points = []
    
    for i in range(len(control_points)):
        if control_points[i][0] < smallest_x:
            smallest_x = control_points[i][0]
        if control_points[i][1] < smallest_y:
            smallest_y = control_points[i][1]
        if control_points[i][2] < smallest_z:
            smallest_z = control_points[i][2]

    return [smallest_x, smallest_y, smallest_z]

def write_centres(smallest_control_points):
    centre_x = "centre_x = " + str(-smallest_control_points[0]) + ";\n"
    centre_y = "centre_y = " + str(-smallest_control_points[1]) + ";\n"
    centre_z = "centre_z = " + str(-smallest_control_points[2]) + ";\n\n"
    return centre_x + centre_y + centre_z

def write_functions():
    init_function = "function init(evt)\n{\n\tif(window.svgDocument == null)\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\tdraw_object();\n}\n\n"

    draw_object = "function draw_object()\n{\n\t"
    return init_function + draw_object

generate_svg("cube.fbx")
