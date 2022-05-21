# One Card Poker Game Simulator

This is a tool to simulate lots of games of "One Card Poker", a much simplified version of poker 
perfect for Game Theory applications. 
Made in Python, used libraries matplotlib for plotting, numpy for storing data, tkinter for GUI, 
colorama for highlighted players in an IDE or other console based python environments.

For humans to play against AI or another player the code needs to run in an IDE or other console 
based python environments.

For rules and more information about the "One Card Poker" game, which this project is based on, 
please refer to this paper:
http://www.swansonsite.com/W/instructional/game_theory.pdf

## Instructions for the main program

### General
- In the top part of the window you can adjust the number of games simulated in the text field. Next
to it, you can adjust more settings in the "Game Settings" tab.
- Under it, you can choose players from the drop down menu, and adjust their settings in the 
  adjacent tab. Not all dropdown options might have a settings tab, some are not adjustable.
- The player option is console based, as mentioned previously, so it needs to be run in a console
  environment or an IDE.
- When you are happy with all the chosen simulation parameters, click the big green "Run" button to 
  run the simulations.
- Cancel and get the results so far by pressing the "Stop" button underneath the "Run" button.
- Bellow you can track your progress looking at the progress bar. 
- When the simulation is done, a time of how long the simulation took will appear 
  above the progress bar.

### Game Settings
- The labels next to the checkboxes are self-explanatory, check the checkboxes associated to the 
  label to activate setting
- The print_portions text field is a bit special. Print portions are how many times the program 
  will update progress bar while running, so having a larger amount for a larger sample size will
  improve the smoothness of the filling up of the progress bar, updating you on the status of 
  the current simulation more often. That may come with a small performance hit, it should be fine 
  as long as you use relatively small numbers compared to the sample size, but that depends on how 
  often you want to receive updates on the simulation progress. Issues with this parameter might 
  come up is the sample size is smaller than the parameter, so try to have the parameter to be
  a smaller number than the sample size.
- There is a save button located in the bottom right corner to save the settings, which should 
  automatically happen when exiting to main menu too.
- The settings are saved to a json file named appropriately, which could be changed instead before 
  staring the program

### Player settings
- When entering the settings menu the window size will extend to encompass all the changeable 
  parameters.
- All changeable parameters come in pairs of three, "f", "c" and "b". "f" stands, for "fold",
  "c" for "check" and "b" for "bet". In this context, "calling" a bet is the same as betting,
  so the related settings have betting option instead because they work logically the same way.
- In first column there are moves for the opener, where one represents when the opener gets a one,
  etc. Then, you can choose how often you should do one of the given actions, relative to each 
  other. For example, if the settings are 0, 1, 0, that means that the distribution will always 
  choose the second option. If the settings are 1, 0, 1, or 0.5, 0, 0.5, then in both cases 
  there will be a 50% chance that the first and last options are going to be chosen. So, to have
  an even distribution one could use settings of 1, 1, 1, or 0.33, 0.33, 0.33, etc.
- In the next column there are even more settings, because you have more information based on 
  opponents move, represented on top.
  The same applies to the last one, and that's all possible reasonable combinations, except for when
  the opponent folds and you win automatically, so there is no need for options there.   
- There is a save button located in the bottom right corner to save the settings, which should 
  automatically happen when exiting to main menu too.
- The settings are saved to a json file named appropriately, which could be changed instead before 
  staring the program
- The settings are saved in different files for each player, so the parameters can be chosen 
  independently even for the same types of AI based players. The settings of the first player
  are saved to files which contain an "1", while settings for the second player are saved to files
  which contain a "2".

### Matplotlib graphing
- For more information about this interactive graphing tool please refer to the matplotlib 
  documentation and their website, or other tutorial/guides on how to use the too.
- The tool should be self-explanatory, where the plus button zooms in and minus zooms out, etc. 
  To save the graph, press the save button down to the left of the center
  
## The News Searcher
- In the news searcher tab you will be greeted with three dropdown menus, with the according 
  labels on top of them, as well as a "Search Articles" button.
- In the "News Outlets" dropdown menu, change the "None" option to one of the presented news 
  outlets to choose it.
- Then, a topic will be automatically chosen in the next dropdown menu. If you would like to 
  change it, select a topic you like in the dropdown menu.
- In the next dropdown menu, you can choose how many articles you would like to be searched and 
  displayed to you. Choosing fewer gives an insignificant increase in performance, because the bulk
  of the wait time comes from the requests to the website.
- When you're done choosing, click the "Search Articles" button, to find articles in the chosen 
  news outlet in the given topic. They will appear in as links right bellow the choosing panel.
- To read more about one of the given articles, hover over the title and click it, which should 
  open a new tab in your browser with your article.
- This obviously requires an internet connection, so make sure you got one before running the 
  searcher.


