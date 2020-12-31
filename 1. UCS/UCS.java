import java.util.*;

public class UCS{
    public static void main(String[] args) {


        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int m = scanner.nextInt();
        int s = scanner.nextInt();
        int t = scanner.nextInt();
        Graph graph = new Graph(n, s, t);
        for (int i = 0; i < m; i++) {
            int v = scanner.nextInt();
            int w = scanner.nextInt();
            int c = scanner.nextInt();
            graph.addEdge(v, w);
            graph.addCost(v, w, c);
        }
        System.out.println(graph.secondSmallestPath());
    }

    static class Graph {
        int numberOfVertices;
        ArrayList<Node>[] neighborsArrayList; // araye e az array list e node ha + be ghesmate 0 kari nadarim
        HashMap<Pair, Integer> costs;
        int initialState;
        int goalState;

        Graph(int n, int initialState, int goalState) {
            numberOfVertices = n;
            neighborsArrayList = new ArrayList[n + 1];
            costs = new HashMap<>();
            this.initialState = initialState;
            this.goalState = goalState;
            for (int i = 0; i < n + 1; i++) {
                neighborsArrayList[i] = new ArrayList<>();
            }
        }

        void addEdge(int v, int w) {        // v->w
            Node node = new Node(w, Integer.MAX_VALUE);
            neighborsArrayList[v].add(node);
        }

        void addCost(int v, int w, int cost) {      //adds new edge cost
            costs.put(new Pair(v, w), cost);
        }

        boolean goalTest(Node x) {
            return x.number == goalState;
        }

        int secondSmallestPath() {

            int numberOfVisitedGoal = 0;
            MinHeap fringe = new MinHeap(1000000);
            fringe.insert(new Node(initialState, 0));
            while (fringe.heap.length != 0) {
                Node state = fringe.findMin();
                fringe.delete();

                if (goalTest(state)) {
                    numberOfVisitedGoal++;
                    if (numberOfVisitedGoal == 2) {
                        return state.f_value;
                    }
                }

                for (Node neighbor : neighborsArrayList[state.number]) {
                    Node newNode = new Node(neighbor.number, neighbor.f_value);
                    newNode.f_value = state.f_value + costs.get(new Pair(state.number, neighbor.number));
                    fringe.insert(newNode);
                }
            }
            return -1;
        }
    }

    static class Node {
        int number;     //number of the node in the main graph
        int f_value;    //the function f for that node

        Node(int number, int f_value) {
            this.number = number;
            this.f_value = f_value;
        }
    }

    static class Pair {
        int key;
        int value;

        Pair(int key, int value) {
            this.key = key;
            this.value = value;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Pair pair = (Pair) o;
            return key == pair.key &&
                    value == pair.value;
        }

        @Override
        public int hashCode() {
            return Objects.hash(key, value);
        }
    }

    static class MinHeap {
        private static final int d = 2;
        private int heapSize;
        private Node[] heap;

        MinHeap(int capacity) {
            heapSize = 0;
            heap = new Node[capacity + 1];
            Arrays.fill(heap, new Node(0, -1));
        }

        private int parent(int i) {
            return (i - 1) / d;
        }

        private int kthChild(int i, int k) {
            return d * i + k;
        }

        void insert(Node x) {
            heap[heapSize++] = x;
            bubbleUp(heapSize - 1);
        }

        Node findMin() {
            return heap[0];
        }


        void delete() {
            heap[0] = heap[heapSize - 1];
            heapSize--;
            bubbleDown();
        }

        private void bubbleUp(int childInd) {
            Node tmp = heap[childInd];
            while (childInd > 0 && tmp.f_value < heap[parent(childInd)].f_value) {
                heap[childInd] = heap[parent(childInd)];
                childInd = parent(childInd);
            }
            heap[childInd] = tmp;
        }

        private void bubbleDown() {
            int child;
            int ind = 0;
            Node tmp = heap[ind];
            while (kthChild(ind, 1) < heapSize) {
                child = minChild(ind);
                if (heap[child].f_value < tmp.f_value)
                    heap[ind] = heap[child];
                else
                    break;
                ind = child;
            }
            heap[ind] = tmp;
        }

        private int minChild(int ind) {
            int bestChild = kthChild(ind, 1);
            int k = 2;
            int pos = kthChild(ind, k);
            while ((k <= d) && (pos < heapSize)) {
                if (heap[pos].f_value < heap[bestChild].f_value)
                    bestChild = pos;
                pos = kthChild(ind, k++);
            }
            return bestChild;
        }

    }

}
