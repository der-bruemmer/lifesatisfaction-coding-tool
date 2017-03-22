# Lifesatisfaction Coding Tool

GUI coding tool to code a number of textual responses according to a predefined coding scheme.

## Usage

The tool first asks for the rater name. 
It then loads a a local data file `data.tsv` and displays the text within in a main window.
Next to the window, it allows the selection of the number of life satisfaction strategies mentioned in the displayed text.
Raters first code the number of strategies, then for each strategy, if they are active or not, how specific they are and if they are social or fatalistic.
Raters can categorize the text if they are no strategies as well.

The tool allows undoing steps, adding commentary, flagging the text as unrateable and flagging it if it allows uniquely identifying the person that wrote it.

After finishing, closing the tool or pressing "save", the tool saves the coding to a tsv file `$ratername.tsv`. It allows resuming if the same rater opens it again.

If you want to use this tool, be aware it was hacked together haphazardly to fulfill a specific purpose.