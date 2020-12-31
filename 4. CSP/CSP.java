import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Scanner;

public class CSP{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        HashMap<Integer, Integer> teamValues = new HashMap<>();
        for (int i = 0; i < 2 * n; i++) {
            int number = scanner.nextInt();
            int value = scanner.nextInt();
            teamValues.put(number, value);
        }
        ArrayList<Node> nodes = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            Node node = new Node(i + 1, teamValues.get(i + 1));
            for (int j = n; j < 2 * n; j++) {
                if (Math.abs(node.value - teamValues.get(j + 1)) <= 2) {
                    node.domain.add(j + 1);
                }
            }
            nodes.add(node);
        }

        // Try to make the domains arc-consistent
        arc_consistency(nodes);
        // This shuffles the node so that it gives all solutions
        Collections.shuffle(nodes);
        backTrack(nodes);

        for (Node node : nodes) {
            if (node.assignedValue == -1) {
                System.out.println("NO");
                System.exit(0);
            }
        }

        while (true) {
            String newLine = scanner.next();
            if (newLine.equals("end")) {
                break;
            }
            int nodeNumber = Integer.parseInt(newLine);
            for (Node node : nodes) {
                if (node.number == nodeNumber) {
                    System.out.println(node.assignedValue);
                    break;
                }
            }
        }
    }


    public static boolean backTrack(ArrayList<Node> nodes) {
        if (isComplete(nodes)) {
            return true;
        }
        Node var = selectUnassigned(nodes);
        if (var != null) {
            for (int i = 0; i < var.domain.size(); i++) {
                int value = var.domain.get(i);
                boolean isConsistent = true;
                for (Node node : nodes) {
                    if (node.assignedValue == value) {
                        isConsistent = false;
                        break;
                    }
                }
                if (isConsistent) {
                    var.assignedValue = value;
                    boolean result = backTrack(nodes);
                    if (result) {
                        // the value has been assigned here!
                        // remove other values from domain and do arc consistency again
                        // arc consistency can be done after each assignment
                        var.domain.clear();
                        var.domain.add(value);
                        arc_consistency(nodes);
                        return true;
                    }
                    var.assignedValue = -1;
                }
            }
        }
        return false;
    }

    public static Node selectUnassigned(ArrayList<Node> nodes) {
        for (Node node : nodes) {
            if (node.assignedValue == -1) {
                return node;
            }
        }
        return null;
    }

    public static boolean isComplete(ArrayList<Node> nodes) {
        boolean isComplete = true;
        for (Node node : nodes) {
            if (node.assignedValue == -1) {
                isComplete = false;
                break;
            }
        }
        return isComplete;
    }

    public static boolean removeInconsistentValues(Node firstNode, Node secondNode) {
        boolean removed = false;
        for (int i = 0; i < firstNode.domain.size(); i++) {
            int x = firstNode.domain.get(i);
            boolean flag = false;
            for (int y : secondNode.domain) {
                if (y != x) {
                    flag = true;
                    break;
                }
            }
            if (!flag) {
                firstNode.domain.remove(Integer.valueOf(x));
                removed = true;
            }
        }
        return removed;
    }

    public static void arc_consistency(ArrayList<Node> nodes) {
        ArrayList<Pair> queue = new ArrayList<>();
        for (int i = 0; i < nodes.size(); i++) {
            for (int j = 0; j < nodes.size(); j++) {
                if (i != j) {
                    Pair pair = new Pair(nodes.get(i), nodes.get(j));
                    queue.add(pair);
                }
            }
        }
        while (!queue.isEmpty()) {
            Pair deQueued = queue.remove(0);
            if (removeInconsistentValues(deQueued.first, deQueued.second)) {
                if (deQueued.first.domain.size() == 0) {
                    return;
                }
                for (int k = 0; k < nodes.size(); k++) {
                    if (k != deQueued.first.number - 1 && k != deQueued.second.number - 1) {
                        Pair newPair = new Pair(nodes.get(k), deQueued.first);
                        queue.add(newPair);
                    }
                }
            }

        }
    }


    static class Pair {
        Node first;
        Node second;

        public Pair(Node first, Node second) {
            this.first = first;
            this.second = second;
        }
    }

    static class Node {
        int number;
        int value;
        int assignedValue;
        ArrayList<Integer> domain;

        public Node(int number, int value) {
            this.number = number;
            this.value = value;
            this.domain = new ArrayList<>();
            this.assignedValue = -1;
        }
    }
}
