import time
import BaseHTTPServer
import FbxCommon

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>FBX Parser</title></head>")
        s.wfile.write("<body>")

        for dirname,dirnames

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
        svg_content += write_faces(mesh)
        svg_content += write_depth(mesh)
        
        control_points = mesh.GetControlPoints()
        smallest_control_points = find_smallest_control_points(control_points)

        svg_content += write_coordinates(control_points, smallest_control_points)
        svg_content += write_centres(smallest_control_points)

        svg_content += write_functions()

    svg_content += "]]>\n</script>\n"

    svg_content += write_paths(mesh)

    svg_content += "\n</svg>"
    
    svg_file = open("box_wire.svg", "w")
    svg_file.write(svg_content)
    svg_file.close()

def write_meta_data():
    svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    svg_content += "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100%\" height=\"100%\" onload=\"init(evt)\">\n"
    #svg_content += "<style>\n.edge{\nfill: white;\nstroke: black;\nstroke-width: 1;\n}\n</style>\n\n"
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
    for i in range(mesh.GetPolygonCount()):
        faces += "["
        for j in range(mesh.GetPolygonSize(i)):
            faces += str(mesh.GetPolygonVertex(i, j)) + ","
        faces = faces[:-1] + "],"
    faces = faces[:-1] + "]\n"
    return faces

def write_depth(mesh):
    depth = "depth = ["
    for i in range(mesh.GetPolygonCount()):
        depth += "0,"
    depth = depth[:-1] + "]\n\n"
    return depth

def write_coordinates(control_points, smallest_control_points):
    x_coordinates = "x_coordinates = ["
    y_coordinates = "y_coordinates = ["
    z_coordinates = "z_coordinates = ["

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
    init_function = "function init(evt)\n{\n\tif(window.svgDocument == null)\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\n\trotate_round_x(0.78);\n\trotate_round_y(0.78);\n\n\tdetermine_depth()\n\tdraw_object();\n\tset_viewport();\n}\n\n"

    draw_object = "function draw_object()\n{\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tvar d = 'M' + x_coordinates[faces[depth[i]][0]] + ' ' + y_coordinates[faces[depth[i]][0]];\n\t\tfor(var j = 1; j < faces[depth[i]].length; j++)\n\t\t{\n\t\t\td += ' ' + 'L' + x_coordinates[faces[depth[i]][j]] + ' ' + y_coordinates[faces[depth[i]][j]];\n\t\t}\n\t\td += ' Z';\n\t\tface.setAttributeNS(null, 'd', d);\n\t}\n}\n\n"

    set_viewport = "function set_viewport()\n{\n\tmin_x = 0;\n\tmax_x = 0;\n\tmin_y = 0;\n\tmax_y = 0;\n\n\tfor(var i = 0; i < x_coordinates.length; i++)\n\t{\n\t\tif(min_x > x_coordinates[i])\n\t\t\tmin_x = x_coordinates[i];\n\t\tif(max_x < x_coordinates[i])\n\t\t\tmax_x = x_coordinates[i];\n\t\tif(min_y > y_coordinates[i])\n\t\t\tmin_y = y_coordinates[i];\n\t\tif(max_y < y_coordinates[i])\n\t\t\tmax_y = y_coordinates[i];\n\t}\n\n\tview_port = document.getElementsByTagName('svg')[0];\n\tview_port.setAttribute('viewBox', min_x + ' ' + min_y + ' ' + (max_x - min_x) + ' ' + (max_y - min_y));\n}\n\n"

    rotate_round_x = "function rotate_round_x(radians)\n{\n\tfor(var i = 0; i < x_coordinates.length; i++)\n\t{\n\t\ty = y_coordinates[i] - centre_y;\n\t\tz = z_coordinates[i] - centre_z;\n\t\td = Math.sqrt(y * y + z * z);\n\t\ttheta = Math.atan2(y, z) + radians;\n\t\ty_coordinates[i] = centre_y + d * Math.sin(theta);\n\t\tz_coordinates[i] = centre_z + d * Math.cos(theta);\n\t}\n}\n\n"

    rotate_round_y = "function rotate_round_y(radians)\n{\n\tfor(var i = 0; i < y_coordinates.length; i++)\n\t{\n\t\tx = x_coordinates[i] - centre_x;\n\t\tz = z_coordinates[i] - centre_z;\n\t\td = Math.sqrt(x * x + z * z);\n\t\ttheta = Math.atan2(x, z) + radians;\n\t\tx_coordinates[i] = centre_x + d * Math.sin(theta);\n\t\tz_coordinates[i] = centre_z + d * Math.cos(theta);\n\t}\n}\n\n"

    determine_depth = "function determine_depth()\n{\n\tvar faces_depth = Array(faces.length);\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tvar depth_value = 0;\n\t\tfor(var j = 0; j < faces[i].length; j++)\n\t\t{\n\t\t\tdepth_value += z_coordinates[faces[i][j]];\n\t\t}\n\t\tdepth_value /= faces[i].length;\n\t\tfaces_depth[i] = depth_value;\n\t}\n\n\tfor(var i = 0; i < depth.length; i++)\n\t{\n\t\tvar closest_face = -1;\n\t\tfor(var j = 0; j < faces_depth.length; j++)\n\t\t{\n\t\t\tif(faces_depth[j] != null && (closest_face == -1 || faces_depth[closest_face] > faces_depth[j]))\n\t\t\t\tclosest_face = j;\n\t\t}\n\t\tdepth[i] = closest_face;\n\t\tfaces_depth[closest_face] = null;\n\t}\n}\n\n"

    return init_function + draw_object + set_viewport + rotate_round_x + rotate_round_y + determine_depth

def write_paths(mesh):
    paths = ""
    start_colour = 0x002BFF
    for i in range(mesh.GetPolygonCount()):
        paths += "\n<path fill='#00" + format(start_colour, 'x') + "' id='face-" + str(i) + "' d=''/>"
        start_colour += 1
    return paths

httpd = BaseHTTPServer.HttpServer(("localhost", 8000), MyHandler)
httpd.serve_forever()

#generate_svg("cube.fbx")
generate_svg("teapot.fbx")
