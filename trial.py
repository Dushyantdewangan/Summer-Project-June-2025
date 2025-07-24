import json
import time
%pip install cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from urllib.request import urlopen

def draw_iss(doblit=True):
    fig, _ = plt.subplots(1, 1)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    if doblit:
        background = fig.canvas.copy_from_bbox(ax.bbox) # cache the background
    plt.ion()
    plt.show()
    while True:
        time.sleep(5)
        req = urlopen("http://api.open-notify.org/iss-now.json")
        obj = json.loads(req.read())
        #print(obj['timestamp'])
        print(float(obj['iss_position']['latitude']), float(obj['iss_position']['longitude']))     
        point = plt.plot([float(obj['iss_position']['longitude'])], 
                            [float(obj['iss_position']['latitude'])],
            color='red', marker='o', markersize=6,
            transform=ccrs.PlateCarree(),
            )
        plt.draw()
        if doblit:
            fig.canvas.restore_region(background) # restore background
            fig.canvas.blit(ax.bbox) # fill in the axes rectangle
        else:
            fig.canvas.draw() # redraw everything
        plt.pause(0.005)
        for p in point:
            p.remove()
if __name__ == '__main__':
    draw_iss(doblit=True)