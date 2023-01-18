import cv2
from PIL import Image, ImageTk
from tkinter import Tk, StringVar, DISABLED, NORMAL
from tkinter.ttk import Frame, Label
from tkinter import Label, Radiobutton, W, Button, IntVar, Frame, TOP, YES, BOTH
from tkinter import filedialog as fd
from tkinter import ttk
from simulation_machado import simulatem, find_areas, find_areas_exp

window_width = 800
window_height = 700
tab_height = window_height - 200

NORMAL_VIEW = 0
PROTANOMALY = 1
DEUTERANOMALY = 2
TRITANOMALY = 3
LIGHT = 4
MEDIUM = 5
STRONG = 6
ACHROMATOPSIA = 7

PROTANOPIA = 5
DEUTERANOPIA = 6
TRITANOPIA = 7

class SimulationGui():

    def ss(self):

        print('ss', self.selected_type, self.selected_level)
        self.selected = self.var.get()

        self.selected_type = int(self.var1.get())
        self.selected_level = int(self.var2.get()) - 4
        res_areas = None
        if self.selected_type == 0:
            sim_image = self.loaded_image.copy()
            sim_image = Image.fromarray(sim_image)
            self.rb_light.configure(state=DISABLED)
            self.rb_medium.configure(state=DISABLED)
            self.rb_strong.configure(state=DISABLED)
        else:
            print('type', self.selected_type)
            print('level', self.selected_level)

            if self.selected_type == ACHROMATOPSIA:
                sim_image = cv2.cvtColor(self.loaded_image, cv2.COLOR_RGB2GRAY)
                self.rb_light.configure(state = DISABLED)
                self.rb_medium.configure(state = DISABLED)
                self.rb_strong.configure(state = DISABLED)
            else:
                self.rb_light.configure(state = NORMAL)
                self.rb_medium.configure(state = NORMAL)
                self.rb_strong.configure(state = NORMAL)
                sim_image = simulatem(self.loaded_image, self.selected_type-1, self.selected_level)
                res_areas = find_areas_exp(self.loaded_image, sim_image)

            self.simul_image = sim_image
            sim_image = Image.fromarray(sim_image)

        self.label_simul.after(10, self.label_simul.destroy())
        img_width, img_height = sim_image.size
        if img_width > img_height:
            fw = img_width / window_width
            h = int(img_height / fw)
            w = window_width
            if h > tab_height:
                fw = tab_height / h
                h = tab_height
                w = int(window_width * fw)
        else:
            h = tab_height
            fh = img_height / h
            w = int(img_width / fh)
        sim_image = sim_image.resize((w, h), Image.ANTIALIAS)
        original_pil = ImageTk.PhotoImage(sim_image)
        self.label_simul = Label(self.tab_simulate, image=original_pil)
        self.label_simul.image = original_pil
        self.label_simul.pack(side=TOP, expand=YES, fill=BOTH)
        if self.tabControl.index(self.tabControl.select()) != 1:
            self.tabControl.select(self.tab_simulate)

        if res_areas is not None:
            res_pil = Image.fromarray(res_areas)
        else:
            res_pil = Image.fromarray(self.loaded_image)
        self.label_fixed.after(10, self.label_fixed.destroy())
        res_pil = res_pil.resize((w, h), Image.ANTIALIAS)
        res_pil2 = ImageTk.PhotoImage(res_pil)
        self.label_fixed = Label(self.tab_fixed, image=res_pil2)
        self.label_fixed.image = res_pil2
        self.label_fixed.pack(side=TOP, expand=YES, fill=BOTH)

    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.var = IntVar()
        self.init_ui()
        self.label_original = None
        self.label_simul = None
        self.label_fixed = None
        self.center = None
        self.loaded_image = None
        self.selected = None
        self.selected_type = 0
        self.selected_level = 0
        self.tab_original = None
        self.tab_simulate = None
        self.tab_fixed = None
        self.tabControl = None
        self.simul_image = None

        print('>>', self.selected_type, self.selected_level)

    def init_ui(self):
        self.simul_image = None
        self.selected_type = 0
        self.selected_level = 0
        self.root.title('CVD Simulation')
        self.root.geometry(f'{window_width}x{window_height}')

        # create all of the main containers
        top_frame = Frame(self.root, bg='white', width=window_width, height=50, pady=3)


        # layout all of the main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.var1 = StringVar()
        self.var2 = StringVar()

        self.var1.set(0)
        self.var2.set(4)

        top_frame.grid(row=0, sticky="ew")
        # create the widgets for the top frame
        # model_label = Label(top_frame, text='Daltonismo')
        # model_label.grid(row=0, column=0, padx=10, pady=3)

        model_label2 = Label(top_frame, text='Anomalous Trichromacy:', bg='white')
        model_label2.grid(row=0, column=1, padx=10, pady=3)

        model_label3 = Label(top_frame, text='Severity:', bg='white')
        model_label3.grid(row=0, column=2, padx=10, pady=3)

        model_label4 = Label(top_frame, text='Monochromatic view:', bg='white')
        model_label4.grid(row=0, column=3, padx=10, pady=3)

        open_button = Button(top_frame, text='Change Image', command=self.select_file)
        open_button.grid(row=0, column=4, padx=10, pady=3)

        save_button = Button(top_frame, text='Save Image', command=self.select_file)
        save_button.grid(row=1, column=4, padx=10, pady=3)


        rb_normal = Radiobutton(top_frame, text='Normal View', variable = self.var1, value=NORMAL_VIEW, command=self.ss, bg='white')
        rb_normal.grid(row=1, column=0, padx=3, pady=3)

        rb_protonamaly = Radiobutton(top_frame, text='Protanomaly', variable = self.var1, value=PROTANOMALY, command=self.ss, bg='white')
        rb_protonamaly.grid(row=1, column=1, padx=3, pady=3)
        r2_1 = Radiobutton(top_frame, text='Deuteranomaly', variable = self.var1, value=DEUTERANOMALY, command=self.ss, bg='white')
        r2_1.grid(row=2, column=1, padx=3, pady=3)
        r3_1 = Radiobutton(top_frame, text='Tritanomaly', variable = self.var1, value=TRITANOMALY, command=self.ss, bg='white')
        r3_1.grid(row=3, column=1, padx=10, pady=3)

        self.rb_light = Radiobutton(top_frame, text='Light', variable = self.var2, value=LIGHT, command=self.ss, bg='white')
        self.rb_light.grid(row=1, column=2, padx=3, pady=3)
        self.rb_medium = Radiobutton(top_frame, text='Moderate', variable = self.var2, value=MEDIUM, command=self.ss, bg='white')
        self.rb_medium.grid(row=2, column=2, padx=3, pady=3)
        self.rb_strong = Radiobutton(top_frame, text='Strong', variable = self.var2, value=STRONG, command=self.ss, bg='white')
        self.rb_strong.grid(row=3, column=2, padx=3, pady=3)
        self.rb_light.configure(state=DISABLED)
        self.rb_medium.configure(state=DISABLED)
        self.rb_strong.configure(state=DISABLED)

        self.rb_achromatopsia = Radiobutton(top_frame, text='Achromatopsia', variable=self.var1, value=ACHROMATOPSIA, command=self.ss, bg='white')
        self.rb_achromatopsia.grid(row=1, column=3, padx=3, pady=3)

        # # layout the widgets in the top frame
        # model_label.grid(row=0, columnspan=3)

        self.center = Frame(self.root, bg='white', width=window_width, height=40, padx=3, pady=3)
        self.tabControl = ttk.Notebook(self.center)
        self.tab_original = ttk.Frame(self.tabControl)
        self.tab_simulate = ttk.Frame(self.tabControl)
        self.tab_fixed = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_original, text='Original Image')
        self.tabControl.add(self.tab_simulate, text='Simulated Image')
        self.tabControl.add(self.tab_fixed, text='Annotated Image')
        self.tabControl.pack(expand=1, fill="both")

        self.center.grid(row=1, sticky="nsew")
        # create the center widgets
        self.center.grid_rowconfigure(1, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        original = Image.open('../imgs/sem.jpg')
        self.loaded_image = cv2.cvtColor(cv2.imread('../imgs/sem.jpg'), cv2.COLOR_BGR2RGB)
        img_width, img_height = original.size
        if img_width >= img_height:
            fw = img_width / window_width
            h = int(img_height / fw)
            w = window_width
            if h > tab_height:
                fw = tab_height / h
                h = tab_height
                w = int(window_width * fw)
        else:
            h = tab_height
            fh = img_height / h
            w = int(img_width / fh)

        original = original.resize((w, h), Image.ANTIALIAS)
        original_pil = ImageTk.PhotoImage(original)
        self.label_original = Label(self.tab_original, image=original_pil, bg='white')
        self.label_original.image = original_pil
        self.label_original.pack(side=TOP, expand=YES, fill=BOTH)

        simul_pil = ImageTk.PhotoImage(original)
        self.label_simul = Label(self.tab_simulate, image=simul_pil, bg='white')
        self.label_simul.image = simul_pil
        self.label_simul.pack(side=TOP, expand=YES, fill=BOTH)

        fixed_pil = ImageTk.PhotoImage(original)
        self.label_fixed = Label(self.tab_fixed, image=fixed_pil, bg='white')
        self.label_fixed.image = fixed_pil
        self.label_fixed.pack(side=TOP, expand=YES, fill=BOTH)

        self.root.mainloop()

    def select_file(self):
        filetypes = (
            ('Image files', '*.jpg *.png'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Escolha uma imagem',
            initialdir='/',
            filetypes=filetypes)
        print(filename)

        self.label_original.after(10, self.label_original.destroy())
        self.loaded_image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        original = Image.fromarray(self.loaded_image)
        img_width, img_height = original.size
        if img_width > img_height:
            fw = img_width / window_width
            h = int(img_height / fw)
            w = window_width
            if h > tab_height:
                fw = tab_height / h
                h = tab_height
                w = int(window_width * fw)
        else:
            h = window_height - 200
            fh = img_height / h
            w = int(img_width / fh)
        original = original.resize((w, h), Image.ANTIALIAS)
        original_pil = ImageTk.PhotoImage(original)
        self.label_original = Label(self.tab_original, image=original_pil)
        self.label_original.image = original_pil
        #self.label_original.grid(row=0, column=0, padx=10, pady=3)
        self.label_original.pack(side=TOP, expand=YES, fill=BOTH)
        self.ss()

    def save_file(self):
        cv2.imwrite('../imgs/semA.jpg', self.simul_image[..., ::-1].copy())

def main():

    SimulationGui()


if __name__ == '__main__':
    main()