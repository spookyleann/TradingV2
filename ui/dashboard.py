import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, df, bias, news, bos, fvg):
        super().__init__(parent)

        self.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(self, text="NASDAQ FUTURES DASHBOARD", font=("Arial", 20)).pack(pady=10)

        # Bias
        ctk.CTkLabel(
            self,
            text=f"Daily Bias: {bias}%",
            text_color="green" if bias > 0 else "red",
            font=("Arial", 16)
        ).pack(pady=5)

        # Chart
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df.index, df["Close"], label="Price")
        ax.set_title("Market Structure")

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # Signals
        signal_text = "\n".join([x[1] for x in bos + fvg][-5:])
        ctk.CTkLabel(self, text=f"Structure Signals:\n{signal_text}").pack(pady=5)

        # News
        ctk.CTkLabel(self, text="Market News").pack(pady=5)
        for n in news:
            ctk.CTkLabel(self, text=f"- {n}", wraplength=400).pack(anchor="w")