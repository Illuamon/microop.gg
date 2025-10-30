import tkinter as tk
from collections import Counter
import settings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from helpers import get_summoner_puuid, get_summoner_info, get_match_ids_by_puuid, match_json, extract_useful_info_from_json, get_tier_and_division

#Tkinter setup
root = tk.Tk()
root.title("MicroOP.gg")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

#summoner name
tk.Label(input_frame, text="Summoner Name:").pack(side=tk.LEFT, padx=5)
summoner_entry = tk.Entry(input_frame)
summoner_entry.pack(side=tk.LEFT)

#summoner tag
tk.Label(input_frame, text='Summoner Tag:').pack(side=tk.LEFT, padx=5)
tag_entry = tk.Entry(input_frame)
tag_entry.pack(side=tk.LEFT)

#region
tk.Label(input_frame, text='Region (eun1, euw1): ').pack(side=tk.LEFT, padx=5)
region_entry = tk.Entry(input_frame)
region_entry.pack(side=tk.LEFT)

#api key
api_input_frame = tk.Frame(root)
api_input_frame.pack(pady=10)

tk.Label(api_input_frame, text="API Key:").pack(side=tk.LEFT, padx=5)
api_entry = tk.Entry(api_input_frame)
api_entry.pack(side=tk.LEFT)

#api key change
def change_api():
    settings.API_KEY = api_entry.get().strip()

canvas = None

#get data and generate graph
def generate_graph():
    global canvas

    summoner_name = summoner_entry.get().strip()
    summoner_tag = tag_entry.get().strip()
    region = region_entry.get().strip()
    if not summoner_name:
        return

    try:
        puuid = get_summoner_puuid(summoner_name, summoner_tag)['puuid']
        _ = get_summoner_info(puuid)
        match_ids = get_match_ids_by_puuid(puuid, 20)
        tier_division = get_tier_and_division(puuid, region)

        game_durations = []
        game_results = []
        champ_played = []
        match_num = []

        for i, match_id in enumerate(match_ids):
            data = match_json(puuid, match_id)
            win, duration, champ = extract_useful_info_from_json(puuid, data)
            game_durations.append(duration)
            game_results.append(win)
            champ_played.append(champ)
            match_num.append(i + 1)

        #stats calculation
        winrate = round(sum(game_results) / len(game_results) * 100, 1)
        average_gameduration = sum(game_durations) // len(game_durations)
        most_played_champ, count = Counter(champ_played).most_common(1)[0]

        #the visual part
        fig, ax = plt.subplots(figsize=(13.5, 6))
        colors = ['blue' if result else 'red' for result in game_results]
        ax.bar(match_num, game_durations, color=colors)
        ax.set_xticks(match_num)
        ax.set_xticklabels([str(num) for num in match_num])
        ax.set_title(f'{summoner_name} - Last 20 Ranked Matches')
        ax.set_xlabel('Match Number (1 = newest)')
        ax.set_ylabel('Duration (minutes)')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        summary_text = (
            f"winrate: {winrate}%\n"
            f"average duration: {average_gameduration} min\n"
            f"most played champ: {most_played_champ} ({count} times)\n"
            f"tier: {tier_division[0]}\n"
            f"division: {tier_division[1]}"
        )

        fig.text(0.76, 0.5, summary_text, fontsize=10, va='center',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.5))
        plt.tight_layout(rect=(0, 0, 0.75, 1))

        #remove previous canvas if it exists
        if canvas:
            canvas.get_tk_widget().destroy()

        #new canvas
        new_canvas = FigureCanvasTkAgg(fig, master=root)
        new_canvas.draw()
        new_canvas.get_tk_widget().pack()
        globals()['canvas'] = new_canvas

    except Exception as e:
        print("Error generating graph:", e)

#button to generate graph
generate_button = tk.Button(root, text="Generate Graph", command=generate_graph)
generate_button.pack(pady=5)

#button to ask for api change
api_button = tk.Button(root, text="Change API KEY", command=change_api)
api_button.pack(pady=10)

root.mainloop()
