import sdl2

class Visualiser():
    """An simple interface to visualise data points on a Canvas using SDL.

    This class shall be used to draw datapoints on a Render window
    which is made possible by PySDL2. The class simply works as a wrapper
    and utilizes those functions only that is required for Visualization.

    Parameters
    ----------
    window_title :`String`
        Title to display on the Render Window.
    
    width :`Integer`
        Width of the Render Window.

    height :`Integer`
        Height of the Render Window.
    """


    viewport = {
        'width': int,
        'height': int
    }

    context = {
        'window': sdl2.SDL_Window(),
        'renderer': sdl2.SDL_Renderer(),
    }

    def __init__(
        self,
        window_title: str,
        width: int, #< width of the render window
        height: int #< height of the render window
    ):
        self.viewport['width'] = width
        self.viewport['height'] = height

        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_EVENTS)

        self.context['window'] = sdl2.SDL_CreateWindow(
            window_title.encode('utf-8'),
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width, height, 0
        )

        self.context['renderer'] = sdl2.SDL_CreateRenderer(
            self.context['window'], -1, 0
        )

    def set_callback(self, fn):
        """Assigns the function provided in the argument as the callback
        when invoked the `paint()` method."""
        self.callback = fn

    def set_palette(
        self,
        foreground: tuple, 
        background: tuple
    ):
        """Defines a palette to use in painting datapoints.

        Two colors must be defined for a palette to form, the foreground 
        color and the background color. Each palette must be qualet of `RGBA`
        (ranging from `0` to `255`). Alpha value controls the opacity of the color.
        """
        if len(foreground) == 4 and len(background) == 4:
            self.color_palette = {
                'foreground': foreground,
                'background': background
            }
        else:
            self.color_palette = {
                'foreground': (0xff, 0xff, 0xff, 0xff),
                'background': (0x00, 0x00, 0x00, 0x00)
            }

    def paint(self, *args):
        """Draws datapoints recieved from the callback function.

        The function invokes a callback set previously and pulls the data
        off the return value and visualises the data as points.
        The callback function must return a tuple consisting `LP_SDL_Point_*`

        
        The rest of the arguments are passed to the callback function. Useful,
        if the Callback Function requires somekind of input.
        """

        (data_points, num_datapoints) = self.callback(*args)
.
        foreground = self.color_palette['foreground']
        background = self.color_palette['background']

        # Draws the background #
        sdl2.SDL_SetRenderDrawColor(
            self.context['renderer'],
            background[0],
            background[1],
            background[2],
            background[3]
        )
        sdl2.SDL_RenderClear(self.context['renderer'])

        # Draws the datapoints as paths #
        sdl2.SDL_SetRenderDrawColor(
            self.context['renderer'],
            foreground[0],
            foreground[1],
            foreground[2],
            foreground[3]
        )
        sdl2.SDL_RenderDrawLines(
            self.context['renderer'],
            data_points,
            num_datapoints
        )

        sdl2.SDL_RenderPresent(self.context['renderer'])


    """Aborts the rendering engine and closes the GUI window.
    """
    def close(self):
        sdl2.SDL_DestroyWindow(self.context['window'])
        sdl2.SDL_DestroyRenderer(self.context['renderer'])