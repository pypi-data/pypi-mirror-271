from pyvisjs import Network, Node, Edge, Options

def main() -> None:

    nd1 = Node(1, "node! 1")
    nd2 = Node(2, "node!! 2")
    nd3 = Node(3, "node!!! 3")
    nd4 = Node(4, "node!!!!!! 4")

    eg1 = Edge(1, 2)
    eg2 = Edge(2, 3)
    eg3 = Edge(3, 4)

    opt = Options(width="100px", height="100px")


    nt = Network("hello")
    nt.apply_data([nd1, nd2, nd3, nd4], [eg1, eg2, eg3], opt)
    nt.render_template(open_in_browser=True, output_filename="C:\\Temp\\output.html")

if __name__ == "__main__":
    main()

