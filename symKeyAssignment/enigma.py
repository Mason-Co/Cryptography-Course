import tkinter as tk
from tkinter import ttk, messagebox
from string import ascii_uppercase

ABC = ascii_uppercase

ROTORS = {
    "I":   ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II":  ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV":  ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V":   ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}
REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}


def idx(c):
    return ord(c) - ord("A")


def make_plugboard(text):
    mapping = list(range(26))
    used = set()

    for pair in text.upper().split():
        if len(pair) != 2 or any(c not in ABC for c in pair):
            raise ValueError(f"Invalid plugboard pair: {pair}")

        a, b = pair
        if a == b or a in used or b in used:
            raise ValueError(f"Invalid or repeated plugboard letter: {pair}")

        used.update(pair)
        mapping[idx(a)], mapping[idx(b)] = idx(b), idx(a)

    if len(used) > 20:
        raise ValueError("The Enigma I plugboard supports at most 10 pairs.")

    return mapping


class Rotor:
    def __init__(self, name, ring, position):
        wiring, notch = ROTORS[name]
        self.wiring = [idx(c) for c in wiring]
        self.inverse = [0] * 26

        for i, value in enumerate(self.wiring):
            self.inverse[value] = i

        self.notch = idx(notch)
        self.ring = idx(ring)
        self.position = idx(position)

    def at_notch(self):
        return self.position == self.notch

    def step(self):
        self.position = (self.position + 1) % 26

    def forward(self, value):
        shifted = (value + self.position - self.ring) % 26
        return (self.wiring[shifted] - self.position + self.ring) % 26

    def backward(self, value):
        shifted = (value + self.position - self.ring) % 26
        return (self.inverse[shifted] - self.position + self.ring) % 26


class Enigma:
    def __init__(self, rotors, rings, positions, reflector, plugs):
        if len(set(rotors)) != 3:
            raise ValueError("Select three different rotors.")

        self.names = tuple(rotors)
        self.rings = tuple(rings)
        self.starts = tuple(positions)
        self.reflector = [idx(c) for c in REFLECTORS[reflector]]
        self.plug_text = plugs
        self.plug = make_plugboard(plugs)
        self.reset()

    def reset(self):
        self.left, self.middle, self.right = [
            Rotor(name, ring, position)
            for name, ring, position in zip(
                self.names, self.rings, self.starts
            )
        ]

    def step(self):
        # Enigma double-step behavior.
        middle_notch = self.middle.at_notch()
        right_notch = self.right.at_notch()

        if middle_notch:
            self.left.step()

        if middle_notch or right_notch:
            self.middle.step()

        self.right.step()

    def encode_letter(self, char):
        if char not in ABC:
            return char

        self.step()
        value = self.plug[idx(char)]

        value = self.right.forward(value)
        value = self.middle.forward(value)
        value = self.left.forward(value)

        value = self.reflector[value]

        value = self.left.backward(value)
        value = self.middle.backward(value)
        value = self.right.backward(value)

        value = self.plug[value]
        return ABC[value]

    def encode(self, text):
        return "".join(self.encode_letter(c) for c in text.upper())

    def window_positions(self):
        return "".join(
            ABC[r.position]
            for r in (self.left, self.middle, self.right)
        )


class EnigmaGUI:
    BG = "#20252B"
    PANEL = "#2B323A"
    FG = "#F0F3F6"
    GREEN = "#58C4A3"
    GOLD = "#E8BD65"
    CABLE = "#EF8F71"

    def __init__(self, root):
        self.root = root
        root.title("Enigma I Cipher Machine")
        root.geometry("1000x780")
        root.minsize(820, 650)
        root.configure(bg=self.BG)

        self.rotor_vars = [
            tk.StringVar(value="I"),
            tk.StringVar(value="II"),
            tk.StringVar(value="III"),
        ]
        self.ring_vars = [tk.StringVar(value="A") for _ in range(3)]
        self.position_vars = [tk.StringVar(value="A") for _ in range(3)]
        self.reflector_var = tk.StringVar(value="B")
        self.plug_var = tk.StringVar(
            value="AV BS CG DL FU HZ IN KM OW RX"
        )
        self.machine = None
        self.lamps = {}

        self.build_ui()
        self.apply_settings()

    def build_ui(self):
        tk.Label(
            self.root, text="ENIGMA I",
            font=("Helvetica", 26, "bold"),
            bg=self.BG, fg=self.GREEN,
        ).pack(pady=(12, 0))

        tk.Label(
            self.root, text="Historical rotor cipher simulator",
            bg=self.BG, fg="#B9C1CA",
        ).pack(pady=(0, 12))

        settings = tk.LabelFrame(
            self.root, text=" MACHINE SETTINGS ",
            bg=self.PANEL, fg=self.GREEN, padx=10, pady=8,
        )
        settings.pack(fill="x", padx=15, pady=(0, 10))

        for col, text in enumerate(("Rotor", "Ring", "Window")):
            tk.Label(
                settings, text=text, bg=self.PANEL, fg=self.FG
            ).grid(row=0, column=col, padx=8)

        for i in range(3):
            ttk.Combobox(
                settings, textvariable=self.rotor_vars[i],
                values=list(ROTORS), state="readonly", width=7,
            ).grid(row=i + 1, column=0, padx=8, pady=2)

            ttk.Combobox(
                settings, textvariable=self.ring_vars[i],
                values=list(ABC), state="readonly", width=7,
            ).grid(row=i + 1, column=1, padx=8, pady=2)

            ttk.Combobox(
                settings, textvariable=self.position_vars[i],
                values=list(ABC), state="readonly", width=7,
            ).grid(row=i + 1, column=2, padx=8, pady=2)

        tk.Label(
            settings, text="Reflector", bg=self.PANEL, fg=self.FG
        ).grid(row=0, column=3, padx=8)

        ttk.Combobox(
            settings, textvariable=self.reflector_var,
            values=list(REFLECTORS), state="readonly", width=6,
        ).grid(row=1, column=3, padx=8)

        tk.Label(
            settings, text="Plugboard pairs",
            bg=self.PANEL, fg=self.FG,
        ).grid(row=2, column=3, padx=8, pady=(5, 0))

        tk.Entry(
            settings, textvariable=self.plug_var, width=28,
            bg="#15191E", fg=self.FG, insertbackground=self.FG,
        ).grid(row=3, column=3, padx=8, pady=4)

        buttons = tk.Frame(settings, bg=self.PANEL)
        buttons.grid(row=4, column=0, columnspan=4, pady=8)

        tk.Button(
            buttons, text="Apply Settings",
            command=self.apply_settings,
            bg=self.GREEN, fg="#101A18", relief="flat",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="Reset Rotors",
            command=self.reset_rotors,
            bg="#46515E", fg=self.FG, relief="flat",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="Encrypt / Decrypt",
            command=self.process_text,
            bg=self.GOLD, fg="#171C22", relief="flat",
        ).pack(side="left", padx=5)

        self.position_display = tk.Label(
            self.root, text="A   A   A",
            font=("Courier", 24, "bold"),
            bg="#101418", fg=self.GREEN, pady=8,
        )
        self.position_display.pack(fill="x", padx=15, pady=(0, 10))

        content = tk.Frame(self.root, bg=self.BG)
        content.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        left = tk.Frame(content, bg=self.BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(
            left, text="INPUT MESSAGE",
            bg=self.BG, fg=self.FG,
        ).pack(anchor="w")

        self.input_box = tk.Text(
            left, height=5, wrap="word",
            bg="#11161B", fg=self.FG,
            insertbackground=self.FG,
            font=("Courier", 12), relief="flat",
        )
        self.input_box.pack(fill="x", pady=5)

        tk.Label(
            left, text="OUTPUT",
            bg=self.BG, fg=self.FG,
        ).pack(anchor="w", pady=(5, 0))

        self.output_box = tk.Text(
            left, height=5, wrap="word",
            bg="#11161B", fg=self.GREEN,
            font=("Courier", 12), relief="flat",
        )
        self.output_box.pack(fill="x", pady=5)

        tk.Button(
            left, text="Clear Text",
            command=self.clear_text,
            bg="#46515E", fg=self.FG, relief="flat",
        ).pack(anchor="w", pady=4)

        tk.Label(
            left, text="LAMPBOARD",
            bg=self.BG, fg=self.GOLD,
        ).pack(anchor="w", pady=(8, 4))

        lamps = tk.Frame(left, bg=self.BG)
        lamps.pack(fill="x")

        for i, char in enumerate(ABC):
            lamp = tk.Label(
                lamps, text=char, width=2,
                bg="#39434C", fg=self.FG,
                font=("Courier", 10, "bold"), pady=5,
            )
            lamp.grid(
                row=i // 13, column=i % 13,
                padx=2, pady=2, sticky="ew",
            )
            self.lamps[char] = lamp

        for i in range(13):
            lamps.grid_columnconfigure(i, weight=1)

        board_frame = tk.LabelFrame(
            content, text=" PLUGBOARD ",
            bg=self.PANEL, fg=self.GREEN, padx=5, pady=5,
        )
        board_frame.pack(side="right", fill="y")

        tk.Label(
            board_frame, text="Cable connections",
            bg=self.PANEL, fg=self.FG,
        ).pack()

        self.canvas = tk.Canvas(
            board_frame, width=300, height=410,
            bg="#171C22", highlightthickness=0,
        )
        self.canvas.pack(pady=5)

        self.status = tk.Label(
            self.root, text="Ready",
            bg=self.BG, fg="#B9C1CA", anchor="w",
        )
        self.status.pack(fill="x", padx=15, pady=(0, 8))

    def apply_settings(self):
        try:
            rotors = tuple(v.get() for v in self.rotor_vars)
            rings = tuple(v.get() for v in self.ring_vars)
            positions = tuple(v.get() for v in self.position_vars)

            self.machine = Enigma(
                rotors, rings, positions,
                self.reflector_var.get(), self.plug_var.get(),
            )
            self.draw_plugboard()
            self.update_positions()
            self.clear_lamps()
            self.status.config(text="Machine settings applied.")

        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))

    def draw_plugboard(self):
        canvas = self.canvas
        canvas.delete("all")

        left_x, right_x = 38, 262
        top_y, spacing = 42, 27
        radius = 10
        coords = {}

        for i, char in enumerate(ABC[:13]):
            coords[char] = (left_x, top_y + i * spacing)

        for i, char in enumerate(ABC[13:]):
            coords[char] = (right_x, top_y + i * spacing)

        canvas.create_text(
            150, 16, text="PATCH PANEL",
            fill=self.GOLD, font=("Helvetica", 10, "bold"),
        )

        mapping = self.machine.plug
        seen = set()
        pairs = 0

        # Draw cables before terminals.
        for i, target in enumerate(mapping):
            if i == target or i in seen:
                continue

            seen.update((i, target))
            pairs += 1
            a, b = ABC[i], ABC[target]
            x1, y1 = coords[a]
            x2, y2 = coords[b]
            bend = 20 if pairs % 2 else -20

            canvas.create_line(
                x1, y1,
                150, y1 + bend,
                150, y2 + bend,
                x2, y2,
                smooth=True, splinesteps=24,
                fill=self.CABLE, width=3,
            )

        for char, (x, y) in coords.items():
            connected = mapping[idx(char)] != idx(char)
            color = self.GOLD if connected else "#53606C"
            text_color = "#171C22" if connected else self.FG

            canvas.create_oval(
                x-radius, y-radius, x+radius, y+radius,
                fill=color, outline="#DCE4EB",
            )
            canvas.create_text(
                x, y, text=char,
                fill=text_color, font=("Courier", 8, "bold"),
            )

        canvas.create_text(
            150, 395, text=f"{pairs} cable pairs connected",
            fill="#B9C1CA", font=("Helvetica", 9),
        )

    def update_positions(self):
        self.position_display.config(
            text="   ".join(self.machine.window_positions())
        )

    def clear_lamps(self):
        for lamp in self.lamps.values():
            lamp.config(bg="#39434C", fg=self.FG)

    def reset_rotors(self):
        if self.machine:
            self.machine.reset()
            self.update_positions()
            self.clear_lamps()
            self.status.config(text="Rotors reset to starting positions.")

    def process_text(self):
        if not self.machine:
            return

        text = self.input_box.get("1.0", "end-1c")
        if not text:
            return

        result = self.machine.encode(text)
        self.output_box.insert("end", result + "\n")

        letters = [c for c in result if c in ABC]
        self.clear_lamps()
        if letters:
            self.lamps[letters[-1]].config(
                bg=self.GOLD, fg="#171C22"
            )

        self.update_positions()
        self.status.config(
            text=f"Processed {len(text)} characters. "
                 f"Rotor windows: {self.machine.window_positions()}"
        )

    def clear_text(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.clear_lamps()
        self.status.config(text="Text cleared; rotor positions unchanged.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop()