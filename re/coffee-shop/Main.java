import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Block {
    private String encoded;

    public Block(String text, int i) {
        text = Block.rotate(text, i);
        text = Block.shift(text, i);
        this.encoded = text;
    }

    @Override
    public String toString() {
        return this.encoded;
    }

    public static String rotate(String string, int rotateFactor) {
        if (string.length() < rotateFactor)
            return string;
        return string.substring(rotateFactor) + string.substring(0, rotateFactor);
    }

    public static String shift(String string, int shiftFactor) {
        char[] result = new char[string.length()];

        for (int i = 0; i < string.length(); i++) {
            char c = string.charAt(i);
            if ('0' <= c && c <= '9')
                result[i] = (char) ((c - '0' + shiftFactor) % ('9' - '0') + '0');
            else if ('a' <= c && c <= 'z')
                result[i] = (char) ((c - 'a' + shiftFactor) % ('z' - 'a') + 'a');
            else if ('A' <= c && c <= 'Z')
                result[i] = (char) ((c - 'A' + shiftFactor) % ('Z' - 'A') + 'A');
            else
                result[i] = c;
        }
        return new String(result);
    }

    public static String buildChain(List<Block> chain) {
        StringBuilder result = new StringBuilder();
        for (Block block : chain) {
            result.append(block.toString());
        }
        return result.toString();
    }

}

class Main {

    public static void main(String[] args) throws IOException {
        Scanner flagScanner = new Scanner(new File("flag.txt"));
        String flag = flagScanner.nextLine();

        ArrayList<Block> chain = new ArrayList<>();
        for (int i = 0; i < flag.length(); i += 4) {
            String substring = flag.substring(i, Math.min(i + 4, flag.length()));
            chain.add(new Block(substring, 3));
        }

        System.out.println(Block.buildChain(chain));

    }

}