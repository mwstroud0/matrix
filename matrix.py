import curses
import random
import time

# Characters for raindrops
# Characters for raindrops, including Hebrew letters
chars = ["ｱ", "ｲ", "ｳ", "ｴ", "ｵ", "ｶ", "ｷ", "ｸ", "ｹ", "ｺ",
         "ｻ", "ｼ", "ｽ", "ｾ", "ｿ", "ﾀ", "ﾁ", "ﾂ", "ﾃ", "ﾄ",
         "ﾅ", "ﾆ", "ﾇ", "ﾈ", "ﾉ", "ﾊ", "ﾋ", "ﾌ", "ﾍ", "ﾎ",
         "□", "▢", "○", "△", "▽", "◇","★", "☆", "◯", "◎",
         "∞", "≡", "≠", "≈", "√", "∑", "∫", "⊙", "⊕", "⊗",
         "Ω", "Δ", "λ", "π", "θ", "φ", "0", "1", "2","3", 
         "4", "5", "6", "7", "8", "9", "Б", "Г", "Д",
         "Ж","И", "Й",  "Ā", "Ē", "Ī", "Ō", "Ū", "Ȳ", 
         "Ḁ", "Ḃ", "Ḅ", "Ċ","α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ",]

def init_colors(tail_length):
    """Initialize color pairs for different shades of green."""
    curses.start_color()
    curses.use_default_colors()

    if curses.COLORS >= 256:
        max_green = 1000  # Brightest green
        min_green = 0    # Dimmest green
        min_rgb = 0      # Small values for red and blue to make it closer to black

        for i in range(tail_length):
            green_intensity = max_green - int(i * (max_green - min_green) / (tail_length - 1))
            curses.init_color(i + 1, min_rgb, green_intensity, min_rgb)
            curses.init_pair(i + 1, i + 1, -1)
    else:
        for i in range(tail_length):
            curses.init_pair(i + 1, curses.COLOR_GREEN, -1)

def resize_grid(grid, width, height):
    """Resize the character grid to match the new terminal dimensions."""
    # Resize each column to the new height
    for col in grid:
        if len(col) < height:
            col.extend(random.choice(chars) for _ in range(height - len(col)))
        else:
            del col[height:]

    # If the grid has fewer columns than the new width, add new columns
    if len(grid) < width:
        for _ in range(width - len(grid)):
            grid.append([random.choice(chars) for _ in range(height)])
    # If the grid has more columns than the new width, truncate extra columns
    elif len(grid) > width:
        del grid[width:]

def draw_rain(stdscr):
    curses.curs_set(0)
    tail_length = 25
    init_colors(tail_length)

    # Each column will store the raindrop position and a character for each row
    columns = []
    char_grid = []  # Grid for storing characters at each row/column position

    while True:
        height, width = stdscr.getmaxyx()

        # Reinitialize grid if the terminal size changes
        if len(columns) != width or len(char_grid) == 0:
            columns = [0] * width
            char_grid = [[random.choice(chars) for _ in range(height)] for _ in range(width)]
        else:
            # Resize the grid if necessary
            resize_grid(char_grid, width, height)

        stdscr.erase()

        for x in range(width):
            # Start a new raindrop
            if columns[x] == 0 and random.randint(0, 1000) < 10:
                columns[x] = 1

            if columns[x] > 0:
                y = columns[x]

                # Draw the leading character of the raindrop
                if 0 <= y < height:
                    char = char_grid[x][y]  # Use the character stored in char_grid
                    try:
                        stdscr.addch(y, x, char, curses.color_pair(1))
                    except curses.error:
                        pass

                # Draw the tail, fading it out gradually
                for k in range(1, tail_length):
                    ty = y - k
                    if 0 <= ty < height:
                        char = char_grid[x][ty]  # Use the stored character for the tail
                        if k < tail_length - 5:  # Fade the character
                            try:
                                stdscr.addch(ty, x, char, curses.color_pair(k + 1))
                            except curses.error:
                                pass
                        else:
                            # Clear the character as it fully fades out
                            try:
                                stdscr.addch(ty, x, ' ')
                            except curses.error:
                                pass

                # Move the raindrop down
                columns[x] += 1

                # Reset the raindrop when it goes off the screen and assign new characters
                if columns[x] - tail_length >= height:
                    columns[x] = 0
                    # After the raindrop has passed, reassign new random characters for that column
                    for ty in range(height):
                        char_grid[x][ty] = random.choice(chars)

        stdscr.refresh()
        time.sleep(0.03)

def main():
    curses.wrapper(draw_rain)

if __name__ == "__main__":
    main()