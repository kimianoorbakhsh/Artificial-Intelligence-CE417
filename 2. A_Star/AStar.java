import java.util.*;

public class AStar{
    private static int m;
    private static int n;

    enum direction {
        VERTICAL, HORIZONTAL
    }

    public static void main(String[] args) {

        ArrayList<Block> blocks = new ArrayList<>(); //blocks.get(0) is always the red one
        Scanner scanner = new Scanner(System.in);
        int k = scanner.nextInt();
        n = scanner.nextInt();
        m = scanner.nextInt();
        for (int i = 0; i < k; i++) {
            int x = scanner.nextInt();
            int y = scanner.nextInt();
            char c = scanner.next().charAt(0);
            int l = scanner.nextInt();
            blocks.add(new Block(i + 1, y, x, c, l));
        }

        State initialState = new State(makeBoard(blocks), blocks);
        initialState.h_value = initialState.heuristicCalculator(initialState);
        int solution = findMinimumSteps(initialState);
        System.out.println(solution);
    }

    private static int[][] makeBoard(ArrayList<Block> blocks) {

        int[][] board = new int[m][n];
        for (Block block : blocks) {
            if (block.direction == direction.HORIZONTAL) {
                for (int k = 0; k < block.length; k++) {
                    board[block.row][block.column + k] = block.number;
                }
            } else {
                for (int k = 0; k < block.length; k++) {
                    board[block.row + k][block.column] = block.number;
                }
            }
        }
        return board;
    }

    private static int[][] copy(int[][] current) {
        int[][] newArray = new int[current.length][current[0].length];
        for (int i = 0; i < current.length; i++)
            System.arraycopy(current[i], 0, newArray[i], 0, current[i].length);
        return newArray;
    }

    private static int findMinimumSteps(State initialState) {


        PriorityQueue<State> fringe = new PriorityQueue<>();
        fringe.add(initialState);
        initialState.g_value = 0;
        initialState.f_value = initialState.g_value + initialState.h_value;
        HashMap<State, Integer> explored = new HashMap<>();

        while (fringe.size() != 0) {
            State state = fringe.poll();
            explored.put(state, state.f_value);

            if (state.goalTest()) {
                return state.g_value + 1;
            }

            ArrayList<State> children = state.createChildren(state);
            for (State neighbor : children) {
                if (explored.containsKey(neighbor)) {
                    continue;
                }
                if (fringe.contains(neighbor)) {
                    int new_g = state.g_value + 1;
                    int new_f = new_g + neighbor.h_value;
                    if (new_f < neighbor.f_value) {
                        neighbor.f_value = new_f;
                    }
                    continue;
                }
                neighbor.g_value = state.g_value + 1;
                neighbor.f_value = neighbor.g_value + neighbor.h_value;
                fringe.add(neighbor);
            }
        }
        return -1;
    }


    static class Block {

        int number;
        int row;
        int column;
        direction direction;
        int length;

        Block(int number, int row, int column, char direction, int length) {
            this.number = number;
            this.row = row;
            this.column = column;
            this.length = length;
            if (direction == 'h') {
                this.direction = SecondQuestion.direction.HORIZONTAL;
            } else {
                this.direction = SecondQuestion.direction.VERTICAL;
            }
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Block block = (Block) o;
            return number == block.number;
        }

        @Override
        public int hashCode() {
            return Objects.hash(number);
        }
    }

    static class State implements Comparable {

        int[][] board;
        int f_value;
        int g_value;
        int h_value;
        String hashString = "";
        ArrayList<Block> blocks;

        State(int[][] board, ArrayList<Block> blocks) {
            this.board = new int[m][n];
            this.board = board;
            this.hashString = createHash(board);
            this.blocks = new ArrayList<>();
            this.blocks = blocks;
        }

        String createHash(int[][] board) {
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < n; j++) {
                    this.hashString = this.hashString.concat(String.valueOf(board[i][j]));
                }
            }
            return this.hashString;
        }

        int heuristicCalculator(State state) {
            ArrayList<Integer> heuristic = new ArrayList<>();
            Block redBlock = null;
            for (Block block : state.blocks) {
                if (block.number == 1) {
                    redBlock = block;
                }
            }
            for (int i = redBlock.column + redBlock.length; i < n; i++) {
                if (board[redBlock.row][i] != 0) {
                    if (!heuristic.contains(board[redBlock.row][i])) {
                        heuristic.add(board[redBlock.row][i]);
                    }
                }
            }
            
            return heuristic.size() / n;
        }

        boolean goalTest() {

            Block redBlock = null;
            for (Block block : this.blocks) {
                if (block.number == 1) {
                    redBlock = block;
                }
            }

            int temp = 0;
            if (redBlock != null) {
                while (redBlock.column + temp + redBlock.length < n) {
                    if (this.board[redBlock.row][redBlock.column + temp + redBlock.length] == 0) {
                        temp++;
                    } else {
                        break;
                    }
                }
                int fromRight = temp;

                return fromRight == n - redBlock.column - redBlock.length;
            }
            return false;

        }

        ArrayList<State> createChildren(State parent) {

            ArrayList<State> children = new ArrayList<>();
            for (Block block : parent.blocks) {
                if (block.direction == direction.HORIZONTAL) {

                    int temp = 1;
                    while (block.column - temp >= 0) {
                        if (parent.board[block.row][block.column - temp] == 0) {
                            temp++;
                        } else {
                            break;
                        }
                    }
                    int fromLeft = temp - 1;
                    temp = 0;
                    while (block.column + temp + block.length < n) {
                        if (parent.board[block.row][block.column + temp + block.length] == 0) {
                            temp++;
                        } else {
                            break;
                        }
                    }
                    int fromRight = temp;

                    ArrayList<Block> tempBlocks;
                    int[][] tempBoard = copy(parent.board);
                    for (int i = 1; i <= fromLeft; i++) {
                        tempBlocks = (ArrayList<Block>) parent.blocks.clone();
                        tempBoard[block.row][block.column - i] = block.number;
                        tempBoard[block.row][block.column - i + block.length] = 0;
                        tempBlocks.remove(block);
                        tempBlocks.add(new Block(block.number, block.row, block.column - i, 'h', block.length));
                        int[][] newBoard = copy(tempBoard);
                        State newState = new State(newBoard, tempBlocks);
                        newState.h_value = heuristicCalculator(newState);
                        children.add(newState);
                    }
                    tempBoard = copy(parent.board);
                    for (int i = 0; i < fromRight; i++) {
                        tempBlocks = (ArrayList<Block>) parent.blocks.clone();
                        tempBoard[block.row][block.column + i] = 0;
                        tempBoard[block.row][block.column + i + block.length] = block.number;
                        tempBlocks.remove(block);
                        tempBlocks.add(new Block(block.number, block.row, block.column + i + 1, 'h', block.length));
                        int[][] newBoard = copy(tempBoard);
                        State newState = new State(newBoard, tempBlocks);
                        newState.h_value = heuristicCalculator(newState);
                        children.add(newState);
                    }

                } else {

                    int temp = 1;
                    while (block.row - temp >= 0) {
                        if (parent.board[block.row - temp][block.column] == 0) {
                            temp++;
                        } else {
                            break;
                        }
                    }
                    int fromTop = temp - 1;
                    temp = 0;
                    while (block.row + temp + block.length < m) {
                        if (parent.board[block.row + temp + block.length][block.column] == 0) {
                            temp++;
                        } else {
                            break;
                        }
                    }
                    int fromBottom = temp;

                    ArrayList<Block> tempBlocks;
                    int[][] tempBoard = copy(parent.board);
                    for (int i = 1; i <= fromTop; i++) {
                        tempBlocks = (ArrayList<Block>) parent.blocks.clone();
                        tempBoard[block.row - i][block.column] = block.number;
                        tempBoard[block.row - i + block.length][block.column] = 0;
                        tempBlocks.remove(block);
                        tempBlocks.add(new Block(block.number, block.row - i, block.column, 'v', block.length));
                        int[][] newBoard = copy(tempBoard);
                        State newState = new State(newBoard, tempBlocks);
                        newState.h_value = heuristicCalculator(newState);
                        children.add(newState);
                    }
                    tempBoard = copy(parent.board);
                    for (int i = 0; i < fromBottom; i++) {
                        tempBlocks = (ArrayList<Block>) parent.blocks.clone();
                        tempBoard[block.row + i][block.column] = 0;
                        tempBoard[block.row + i + block.length][block.column] = block.number;
                        tempBlocks.remove(block);
                        tempBlocks.add(new Block(block.number, block.row + i + 1, block.column, 'v', block.length));
                        int[][] newBoard = copy(tempBoard);
                        State newState = new State(newBoard, tempBlocks);
                        newState.h_value = heuristicCalculator(newState);
                        children.add(newState);
                    }
                }
            }


            return children;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            State state = (State) o;
            return Objects.equals(hashString, state.hashString);
        }

        @Override
        public int hashCode() {
            return Objects.hash(hashString);
        }

        @Override
        public int compareTo(Object o) {
            if (o instanceof State) {
                return Integer.compare(this.f_value, ((State) o).f_value);
            }
            return 0;
        }
    }
}