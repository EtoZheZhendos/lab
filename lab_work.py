import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class LabWorkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа № 1 - Электрические измерения")
        self.root.geometry("1200x800")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_table_13_tab()
        self.create_table_14_tab()
        self.create_table_15_tab()
        self.create_graphs_tab()
        
    def create_table_13_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Таблица 1.3 - Напряжения')
        
        ttk.Label(tab, text="Результаты измерений напряжений", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(tab)
        frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        headers = ['Напряжение\nисточника\nпитания, В', 'Предел\nизмерения\nПИ, В', 
                   'Измеренное\nзначение, В', 'Число\nделений\nшкалы', 
                   'Цена\nделения\nВ/д', 'Класс\nточности\n%', 
                   'Абсолютная\nпогрешность\nΔU', 'Относительная\nпогрешность\n%']
        
        for col, header in enumerate(headers):
            ttk.Label(frame, text=header, relief='solid', width=15, 
                     anchor='center', borderwidth=1).grid(row=0, column=col, 
                     sticky='nsew', padx=1, pady=1)
        
        self.table_13_entries = {}
        sources = ['U1', 'U2', 'U3']
        
        for row, source in enumerate(sources, start=1):
            ttk.Label(frame, text=source, relief='solid', width=15, 
                     anchor='center', borderwidth=1).grid(row=row, column=0, 
                     sticky='nsew', padx=1, pady=1)
            
            self.table_13_entries[source] = {}
            col_names = ['predel', 'izmerenie', 'num_deleniy', 'tsena', 'klass', 
                        'abs_pogr', 'otn_pogr']
            readonly_fields = ['tsena', 'abs_pogr', 'otn_pogr']
            
            for col, col_name in enumerate(col_names, start=1):
                entry = ttk.Entry(frame, width=15, justify='center')
                if col_name in readonly_fields:
                    entry.config(state='readonly')
                if col_name == 'predel' or col_name == 'num_deleniy':
                    entry.bind('<KeyRelease>', lambda e, s=source: self.calculate_tsena_13(s))
                entry.grid(row=row, column=col, padx=1, pady=1)
                self.table_13_entries[source][col_name] = entry
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Вычислить погрешности", 
                  command=self.calculate_table_13).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Очистить", 
                  command=self.clear_table_13).pack(side='left', padx=5)
    
    def calculate_tsena_13(self, source):
        try:
            entries = self.table_13_entries[source]
            predel_str = entries['predel'].get()
            num_deleniy_str = entries['num_deleniy'].get()
            
            if predel_str and num_deleniy_str:
                predel = float(predel_str)
                num_deleniy = float(num_deleniy_str)
                
                if num_deleniy != 0:
                    tsena = predel / num_deleniy
                    entries['tsena'].config(state='normal')
                    entries['tsena'].delete(0, tk.END)
                    entries['tsena'].insert(0, f"{tsena:.6f}")
                    entries['tsena'].config(state='readonly')
        except (ValueError, ZeroDivisionError):
            pass
        
    def create_table_14_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Таблица 1.4 - Сопротивления')
        
        ttk.Label(tab, text="Результаты измерений сопротивлений", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(tab)
        frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        headers = ['Сопротив-\nления', 'I\nА', 'U\nВ', 
                   'ΔI\nА', 'δI\n%', 'ΔU\nВ', 'δU\n%', 
                   'Rx\nОм', 'ΔRx\nОм', 'δRx\n%', 'R0\nОм']
        
        ttk.Label(frame, text='Данные измерений', relief='solid', 
                 borderwidth=1).grid(row=0, column=1, columnspan=2, 
                 sticky='nsew', padx=1, pady=1)
        ttk.Label(frame, text='Расчётные данные', relief='solid', 
                 borderwidth=1).grid(row=0, column=3, columnspan=8, 
                 sticky='nsew', padx=1, pady=1)
        
        for col, header in enumerate(headers):
            ttk.Label(frame, text=header, relief='solid', width=10, 
                     anchor='center', borderwidth=1).grid(row=1, column=col, 
                     sticky='nsew', padx=1, pady=1)
        
        self.table_14_entries = {}
        resistors = ['R3', 'R4']
        
        for row, resistor in enumerate(resistors, start=2):
            ttk.Label(frame, text=resistor, relief='solid', width=10, 
                     anchor='center', borderwidth=1).grid(row=row, column=0, 
                     sticky='nsew', padx=1, pady=1)
            
            self.table_14_entries[resistor] = {}
            col_names = ['I', 'U', 'dI', 'dI_rel', 'dU', 'dU_rel', 
                        'Rx', 'DRx', 'dRx', 'R0']
            readonly_fields = ['dI_rel', 'dU_rel', 'Rx', 'DRx', 'dRx', 'R0']
            
            for col, col_name in enumerate(col_names, start=1):
                entry = ttk.Entry(frame, width=10, justify='center')
                if col_name in readonly_fields:
                    entry.config(state='readonly')
                entry.grid(row=row, column=col, padx=1, pady=1)
                self.table_14_entries[resistor][col_name] = entry
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Вычислить сопротивления", 
                  command=self.calculate_table_14).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Очистить", 
                  command=self.clear_table_14).pack(side='left', padx=5)
        
    def create_table_15_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Таблица 1.5 - Мощность')
        
        ttk.Label(tab, text="Измеренные и вычисленные значения мощности, тока и напряжения", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(tab)
        frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        headers = ['I\nА', 'U\nВ', 'Pк\nВт\nКосв ИЗМ', 
                   'ΔU\nВ', 'ΔI\nмА', 'ΔPк\nВт\nКосв изм',
                   'δI\n%', 'δU\n%', 'δP\n%',
                   'Pк\nВт', 'ΔPк\nВт', 'δPк\n%']
        
        ttk.Label(frame, text='Эксперим. данные', relief='solid', 
                 borderwidth=1).grid(row=0, column=0, columnspan=3, 
                 sticky='nsew', padx=1, pady=1)
        ttk.Label(frame, text='Расчёт погрешностей', relief='solid', 
                 borderwidth=1).grid(row=0, column=3, columnspan=3, 
                 sticky='nsew', padx=1, pady=1)
        ttk.Label(frame, text='Расчётные данные', relief='solid', 
                 borderwidth=1).grid(row=0, column=6, columnspan=6, 
                 sticky='nsew', padx=1, pady=1)
        
        ttk.Label(frame, text='Косвенные измерен.', relief='solid', 
                 borderwidth=1).grid(row=1, column=6, columnspan=3, 
                 sticky='nsew', padx=1, pady=1)
        ttk.Label(frame, text='Прямые измерения', relief='solid', 
                 borderwidth=1).grid(row=1, column=9, columnspan=3, 
                 sticky='nsew', padx=1, pady=1)
        
        for col, header in enumerate(headers):
            ttk.Label(frame, text=header, relief='solid', width=10, 
                     anchor='center', borderwidth=1).grid(row=2, column=col, 
                     sticky='nsew', padx=1, pady=1)
        
        self.table_15_entries = []
        
        for row in range(5):
            row_entries = {}
            col_names = ['I', 'U', 'P_indirect', 
                        'dU', 'dI_mA', 'DP_indirect',
                        'dI_rel', 'dU_rel', 'dP_rel',
                        'P_direct', 'DP_direct', 'dP_direct_rel']
            readonly_fields = ['DP_indirect', 'dI_rel', 'dU_rel', 'dP_rel',
                             'dP_direct_rel']
            
            for col, col_name in enumerate(col_names):
                entry = ttk.Entry(frame, width=10, justify='center')
                if col_name in readonly_fields:
                    entry.config(state='readonly')
                entry.grid(row=row+3, column=col, padx=1, pady=1)
                row_entries[col_name] = entry
            
            self.table_15_entries.append(row_entries)
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Вычислить мощность", 
                  command=self.calculate_table_15).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Очистить", 
                  command=self.clear_table_15).pack(side='left', padx=5)
        
    def create_graphs_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Графики')
        
        ttk.Label(tab, text="Графики зависимостей", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Построить U = f(I)", 
                  command=self.plot_u_vs_i).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Построить P = f(I)", 
                  command=self.plot_p_vs_i).pack(side='left', padx=5)
        
        self.canvas_frame = ttk.Frame(tab)
        self.canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    def calculate_table_13(self):
        try:
            for source, entries in self.table_13_entries.items():
                izmerenie = entries['izmerenie'].get()
                klass = entries['klass'].get()
                predel = entries['predel'].get()
                
                if izmerenie and klass and predel:
                    U = float(izmerenie)
                    K = float(klass)
                    U_max = float(predel)
                    
                    delta_U = (K * U_max) / 100
                    entries['abs_pogr'].config(state='normal')
                    entries['abs_pogr'].delete(0, tk.END)
                    entries['abs_pogr'].insert(0, f"{delta_U:.4f}")
                    entries['abs_pogr'].config(state='readonly')
                    
                    if U != 0:
                        otn_pogr = (delta_U / U) * 100
                        entries['otn_pogr'].config(state='normal')
                        entries['otn_pogr'].delete(0, tk.END)
                        entries['otn_pogr'].insert(0, f"{otn_pogr:.4f}")
                        entries['otn_pogr'].config(state='readonly')
                        
            messagebox.showinfo("Успешно", "Погрешности вычислены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
    
    def clear_table_13(self):
        for entries in self.table_13_entries.values():
            for key, entry in entries.items():
                if key not in ['tsena', 'abs_pogr', 'otn_pogr']:
                    entry.delete(0, tk.END)
                else:
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.config(state='readonly')
    
    def calculate_table_14(self):
        try:
            r3_data = {}
            r4_data = {}
            
            for resistor, entries in self.table_14_entries.items():
                I_str = entries['I'].get()
                U_str = entries['U'].get()
                dI_str = entries['dI'].get()
                dU_str = entries['dU'].get()
                
                if I_str and U_str:
                    I = float(I_str)
                    U = float(U_str)
                    
                    if resistor == 'R3':
                        r3_data = {'I': I, 'U': U}
                    elif resistor == 'R4':
                        r4_data = {'I': I, 'U': U}
                    
                    if I != 0:
                        Rx = U / I
                        entries['Rx'].config(state='normal')
                        entries['Rx'].delete(0, tk.END)
                        entries['Rx'].insert(0, f"{Rx:.1f}")
                        entries['Rx'].config(state='readonly')
                        
                        if dI_str and dU_str:
                            dI = float(dI_str)
                            dU = float(dU_str)
                            
                            dI_rel_percent = (dI / I) * 100 if I != 0 else 0
                            dU_rel_percent = (dU / U) * 100 if U != 0 else 0
                            
                            entries['dI_rel'].config(state='normal')
                            entries['dI_rel'].delete(0, tk.END)
                            entries['dI_rel'].insert(0, f"{dI_rel_percent:.2f}")
                            entries['dI_rel'].config(state='readonly')
                            
                            entries['dU_rel'].config(state='normal')
                            entries['dU_rel'].delete(0, tk.END)
                            entries['dU_rel'].insert(0, f"{dU_rel_percent:.2f}")
                            entries['dU_rel'].config(state='readonly')
                            
                            dRx_rel_percent = dU_rel_percent + dI_rel_percent
                            DRx = Rx * (dRx_rel_percent / 100)
                            
                            entries['DRx'].config(state='normal')
                            entries['DRx'].delete(0, tk.END)
                            entries['DRx'].insert(0, f"{DRx:.1f}")
                            entries['DRx'].config(state='readonly')
                            
                            entries['dRx'].config(state='normal')
                            entries['dRx'].delete(0, tk.END)
                            entries['dRx'].insert(0, f"{dRx_rel_percent:.2f}")
                            entries['dRx'].config(state='readonly')
            
            if r3_data and r4_data and 'I' in r3_data and 'I' in r4_data:
                I3 = r3_data['I']
                I4 = r4_data['I']
                U3 = r3_data['U']
                U4 = r4_data['U']
                
                if I3 != I4:
                    R0 = (U4 - U3) / (I3 - I4)
                    for resistor in ['R3', 'R4']:
                        entries = self.table_14_entries[resistor]
                        entries['R0'].config(state='normal')
                        entries['R0'].delete(0, tk.END)
                        entries['R0'].insert(0, f"{R0:.1f}")
                        entries['R0'].config(state='readonly')
                            
            messagebox.showinfo("Успешно", "Сопротивления вычислены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
    
    def clear_table_14(self):
        for entries in self.table_14_entries.values():
            for key, entry in entries.items():
                if key not in ['dI_rel', 'dU_rel', 'Rx', 'dRx', 'DRx', 'R0']:
                    entry.delete(0, tk.END)
                else:
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.config(state='readonly')
    
    def calculate_table_15(self):
        try:
            for row_entries in self.table_15_entries:
                I_str = row_entries['I'].get()
                U_str = row_entries['U'].get()
                P_indirect_str = row_entries['P_indirect'].get()
                dU_str = row_entries['dU'].get()
                dI_mA_str = row_entries['dI_mA'].get()
                P_direct_str = row_entries['P_direct'].get()
                DP_direct_str = row_entries['DP_direct'].get()
                
                if I_str and U_str and dU_str and dI_mA_str:
                    I = float(I_str)
                    U = float(U_str)
                    dU = float(dU_str)
                    dI_mA = float(dI_mA_str)
                    
                    dI_A = dI_mA / 1000
                    
                    dI_rel_percent = (dI_A / I) * 100 if I != 0 else 0
                    dU_rel_percent = (dU / U) * 100 if U != 0 else 0
                    dP_rel_percent = dI_rel_percent + dU_rel_percent
                    
                    row_entries['dI_rel'].config(state='normal')
                    row_entries['dI_rel'].delete(0, tk.END)
                    row_entries['dI_rel'].insert(0, f"{dI_rel_percent:.2f}")
                    row_entries['dI_rel'].config(state='readonly')
                    
                    row_entries['dU_rel'].config(state='normal')
                    row_entries['dU_rel'].delete(0, tk.END)
                    row_entries['dU_rel'].insert(0, f"{dU_rel_percent:.2f}")
                    row_entries['dU_rel'].config(state='readonly')
                    
                    row_entries['dP_rel'].config(state='normal')
                    row_entries['dP_rel'].delete(0, tk.END)
                    row_entries['dP_rel'].insert(0, f"{dP_rel_percent:.2f}")
                    row_entries['dP_rel'].config(state='readonly')
                    
                    if P_indirect_str:
                        P_indirect = float(P_indirect_str)
                        DP_indirect = P_indirect * (dP_rel_percent / 100)
                        row_entries['DP_indirect'].config(state='normal')
                        row_entries['DP_indirect'].delete(0, tk.END)
                        row_entries['DP_indirect'].insert(0, f"{DP_indirect:.3f}")
                        row_entries['DP_indirect'].config(state='readonly')
                    
                    if P_direct_str and DP_direct_str:
                        P_direct = float(P_direct_str)
                        DP_direct_val = float(DP_direct_str)
                        dP_direct_rel_percent = (DP_direct_val / P_direct) * 100 if P_direct != 0 else 0
                        row_entries['dP_direct_rel'].config(state='normal')
                        row_entries['dP_direct_rel'].delete(0, tk.END)
                        row_entries['dP_direct_rel'].insert(0, f"{dP_direct_rel_percent:.2f}")
                        row_entries['dP_direct_rel'].config(state='readonly')
                        
            messagebox.showinfo("Успешно", "Мощность вычислена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
    
    def clear_table_15(self):
        readonly_fields = ['DP_indirect', 'dI_rel', 'dU_rel', 'dP_rel', 
                         'dP_direct_rel']
        for row_entries in self.table_15_entries:
            for key, entry in row_entries.items():
                if key not in readonly_fields:
                    entry.delete(0, tk.END)
                else:
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.config(state='readonly')
    
    def plot_u_vs_i(self):
        try:
            I_values = []
            U_values = []
            
            for row_entries in self.table_15_entries:
                I_str = row_entries['I'].get()
                U_str = row_entries['U'].get()
                
                if I_str and U_str:
                    I_values.append(float(I_str))
                    U_values.append(float(U_str))
            
            if not I_values or not U_values:
                messagebox.showwarning("Предупреждение", 
                                      "Введите данные в таблицу 1.5")
                return
            
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(I_values, U_values, 'bo-', linewidth=2, markersize=8)
            ax.set_xlabel('Ток I, А', fontsize=12)
            ax.set_ylabel('Напряжение U, В', fontsize=12)
            ax.set_title('Зависимость U = f(I)', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка построения графика: {str(e)}")
    
    def plot_p_vs_i(self):
        try:
            I_values = []
            P_values = []
            
            for row_entries in self.table_15_entries:
                I_str = row_entries['I'].get()
                P_str = row_entries['P_indirect'].get()
                
                if not P_str:
                    P_str = row_entries['P_direct'].get()
                
                if I_str and P_str:
                    I_values.append(float(I_str))
                    P_values.append(float(P_str))
            
            if not I_values or not P_values:
                messagebox.showwarning("Предупреждение", 
                                      "Введите данные в таблицу 1.5 и вычислите мощность")
                return
            
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(I_values, P_values, 'ro-', linewidth=2, markersize=8)
            ax.set_xlabel('Ток I, А', fontsize=12)
            ax.set_ylabel('Мощность P, Вт', fontsize=12)
            ax.set_title('Зависимость P = f(I)', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка построения графика: {str(e)}")


def main():
    root = tk.Tk()
    app = LabWorkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

