from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import tkSimpleDialog
import csv
import os
import collections

root = Tk()

class NameDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text="Rater Name:").grid(row=0)
        self.e = Entry(master)
        self.e.grid(row=0, column=1)
        return self.e 

    def apply(self):
        name = str(self.e.get())
        self.result = name
		
class CodingWindow(Frame):


    def __init__(self, master, rater = "no_rater_name"):
        Frame.__init__(self, master)
        filename = "./data.tsv"
        self.texts = self.readTexts(filename)
        self.cur = 0
        self.data = collections.OrderedDict()
        self.identVar = IntVar()
        self.dontknow = IntVar()
        self.zufrieden = IntVar()
        self.resignation = IntVar()
        self.weiterso = IntVar()
        self.anderes = IntVar()
        self.active = IntVar()
        self.topicNumber = IntVar()
        self.topicNumber.set(1) 
        self.ratingData = collections.OrderedDict()
        
        self.grid()
        self.master = master        
        self.master.title("Text Coding")
        
        self.textField = Entry(self, width=15)
        self.textField.grid(row = 0, column = 0, sticky=W)
        if rater is None:
            rater = "no_rater_name"
        else:
            if len(rater) == 0:
                rater = "no_rater_name"
        self.textField.insert(10,rater)
        resumeButton = Button(self, text='resume',command=lambda: self.resume(),width=5)
        resumeButton.grid(row = 0, column = 1, sticky=W)
        #make this save        
        #backButton = Button(self, text='back',command=lambda: self.back())
        #backButton.grid(row = 0, column = 2, sticky=W) 

        quitButton = Button(self, text='save',command=lambda: self.printData())
        quitButton.grid(row = 0, column = 2, sticky=W)  

        identifyable = Checkbutton(self, text = "Person identifizierbar", variable = self.identVar)
        identifyable.grid(row = 5, column = 0, sticky = W,columnspan=3)

        self.rateBox = Frame(self, height=230,width=150)
        self.rateBox.grid_propagate(False)
        self.rateBox.grid(row=2,column=5,rowspan=4,sticky=NW,padx=5)
        naButton = Button(self, text='nicht bewertbar',command=lambda: self.rateText(0))
        naButton.grid(row = 5, column = 1,columnspan=3,sticky=W)
        
        #devider = Frame(self, height=2, bd=1, relief=SUNKEN,width=800,padx=10)
        #devider.grid(row=6,column=0,columnspan=4)
        Label(self,text="Kommentar: ").grid(row=3,column=0,sticky=W)
        self.comment = Text(self, font = "Helvetica 14",wrap=WORD,height=2,width=70)
        self.comment.grid(row=4, column=0, columnspan = 4, sticky = W)
        self.setText(True)
        if os.path.isfile("./"+rater+".csv"):
            self.resume()
        #rateButton = Button(self, text='bewerten',command=lambda: self.rateText(self.topicNumber.get()))
        #rateButton.grid(row = 4, column = 1,columnspan=3,sticky=W)
        

    def makeRatingFrame(self):
        self.resetRateBox()
        self.comment.delete(1.0,END)
        ratingLabel = Label(self.rateBox, text='Anzahl Ideen im Text:',justify=LEFT)
        ratingLabel.grid(row = 0, column = 0, columnspan=2, pady=5, sticky = W)
        for item in [0, 1, 2, 3, 4, 5]:        
            Radiobutton(self.rateBox, text=str(item),variable=self.topicNumber,value=item).grid(row = 1+item, column = 0,columnspan=2, sticky = W)
        backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(0,-1,-1,-1),width=5)
        backButton.grid(row = 8, column = 0, sticky=SW)
        weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.updateRatingFrame(self.topicNumber.get(),self.topicNumber.get(),-1,-1),width=5)
        self.rateBox.rowconfigure(7, weight=1)
        weiterButton.grid(row = 8, column = 1, sticky=SW)   

    def readTexts(self, filename):
        texts = []
        with open(filename, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                texts.append([row[0],row[1]])
        return texts

    def updateRatingFrame(self, textTopics, topicCount, isActive, activityType):       
        self.resetRateBox()
        strategyNo = str(textTopics-topicCount+1)
        data = self.ratingData[str(self.texts[self.cur][0])]
       # print("updateratingframe:"+strategyNo)
       # print(isActive)

        #setting activity value
        defaultActive = 1
        if "active"+strategyNo in data:
            if data["active"+strategyNo] != -1:
                defaultActive = data["active"+strategyNo]

        #setting other values
        defaultDontknow = 0
        defaultZufrieden = 0
        defaultResignation = 0
        defaultWeiterso = 0
        defaultAnderes = 0
        if "dontknow" in data:   
            if data["dontknow"] != -1:
                defaultDontknow = data["dontknow"]
                defaultZufrieden = data["zufrieden"]
                defaultResignation = data["resignation"]
                defaultWeiterso = data["weiterso"]
                defaultAnderes = data["anderes"]

        #persisting previous activity decision
        previousStrat = str(textTopics-topicCount)
        if isActive == 0:
        #    data = {"active"+strategyNo:0,"activeType"+strategyNo:-1,"passiveType"+strategyNo:activityType}
            previousStrat = str(textTopics-topicCount)
            data["active"+previousStrat] = isActive
         #   print("Data")
          #  print(isActive)
         #   print(activityType)
            data["activeType"+previousStrat] = -1
            data["passiveType"+previousStrat] = activityType
            data["dontknow"] = -1
            data["zufrieden"] = -1
            data["resignation"] = -1
            data["weiterso"] = -1
            data["anderes"] = -1
            self.ratingData[str(self.texts[self.cur][0])].update(data)
        elif isActive == 1:
        #    data = {"active"+strategyNo:1,"activeType"+strategyNo:activityType,"passiveType"+strategyNo:-1}
            data["active"+previousStrat] = isActive
        #    print("Data")
        #    print(isActive)
        #    print(activityType)
            data["activeType"+previousStrat] = activityType  
            data["passiveType"+previousStrat] = -1
            data["dontknow"] = -1
            data["zufrieden"] = -1
            data["resignation"] = -1
            data["weiterso"] = -1
            data["anderes"] = -1
            self.ratingData[str(self.texts[self.cur][0])].update(data)
      #  print("saved")
      #  print(self.ratingData[str(self.texts[self.cur][0])])

        if topicCount == 0 and textTopics != 0:
            #save
            self.rateText(1)
            return
        if textTopics == 0:
            self.dontknow.set(defaultDontknow)
            self.zufrieden.set(defaultZufrieden)
            self.resignation.set(defaultResignation)
            self.weiterso.set(defaultWeiterso)
            self.anderes.set(defaultAnderes)
            Checkbutton(self.rateBox, text = "weiß nicht", variable = self.dontknow).grid(row = 0, column = 0,columnspan=2, sticky = W, pady=5)
            Checkbutton(self.rateBox, text = "bin zufrieden", variable = self.zufrieden).grid(row = 1, column = 0,columnspan=2, sticky = W, pady=5)
            Checkbutton(self.rateBox, text = "Resignation", variable = self.resignation).grid(row = 2, column = 0,columnspan=2, sticky = W, pady=5)
            Checkbutton(self.rateBox, text = "weiter wie bisher", variable = self.weiterso).grid(row = 3, column = 0,columnspan=2, sticky = W, pady=5)
            Checkbutton(self.rateBox, text = "anderes", variable = self.anderes).grid(row = 4, column = 0,columnspan=2, sticky = W, pady=5)
            self.rateBox.rowconfigure(5, weight=1)
            #save
            backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(1,-1,-1,-1),width=5)
            backButton.grid(row = 6, column = 0, sticky=SW)    
            weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.rateText(1),width=5)
            weiterButton.grid(row = 6, column = 1, sticky=SW)
        elif textTopics > 0:
            self.active.set(defaultActive)
            Label(self.rateBox,text="Strategie "+strategyNo).grid(row=0, column = 0,columnspan=2, sticky = W,pady=5)
            Label(self.rateBox,text="Aktive Strategie?").grid(row=1, column = 0,columnspan=2, sticky = W,pady=5)
            Radiobutton(self.rateBox, text="ja",variable=self.active,value=1).grid(row = 2, column = 0,columnspan=2,sticky = W)
            Radiobutton(self.rateBox, text="nein",variable=self.active,value=0).grid(row = 3, column = 0,columnspan=2,sticky = W)
            self.rateBox.rowconfigure(4, weight=1)
            backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(1,-1,textTopics, topicCount),width=5)
            backButton.grid(row = 5, column = 0, sticky=SW)
            weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.activeRating(self.active.get(),textTopics,topicCount),width=5)
            weiterButton.grid(row = 5, column = 1, sticky=SW)
    
    def resetRateBox(self):
        for widget in self.rateBox.winfo_children():
            widget.destroy()
        for i in range(0,9):
            self.rateBox.rowconfigure(i, weight=0)

    def activeRating(self,active,textTopics,topicCount):
        cacheData = self.ratingData[str(self.texts[self.cur][0])]
       # print(cacheData)
        self.resetRateBox()
        strategyNo = str(textTopics-topicCount+1)
        #setting default values
        #print("strat:"+str(strategyNo))
        #print("active"+str(active))
        defaultActiveType = 0
        if active == 1:
            if "activeType"+strategyNo in cacheData:
                if cacheData["activeType"+strategyNo] != -1:
                    defaultActiveType = cacheData["activeType"+strategyNo] 
                    #print("activity:"+str(defaultActiveType))
        defaultPassiveType = 0
        if active == 0:
            if "passiveType"+strategyNo in cacheData:
                if cacheData["passiveType"+strategyNo] != -1:
                    defaultPassiveType = cacheData["passiveType"+strategyNo]

        if active == 1:
            self.activeType = IntVar()
            self.activeType.set(defaultActiveType)
            Label(self.rateBox,text="Strategie "+strategyNo).grid(row=0, column = 0,columnspan=2, sticky = W,pady=5)
            Label(self.rateBox,text="Wie konkret?").grid(row=1, column = 0,columnspan=2, sticky = W,pady=5)
            Radiobutton(self.rateBox, text="unspezifisch",variable=self.activeType,value=0).grid(row = 2, column = 0,columnspan=2,sticky = W)
            Radiobutton(self.rateBox, text="mittel",variable=self.activeType,value=1).grid(row = 3, column = 0,columnspan=2,sticky = W)
            Radiobutton(self.rateBox, text="konkret",variable=self.activeType,value=2).grid(row = 4, column = 0,columnspan=2,sticky = W)
            self.rateBox.rowconfigure(5, weight=1)
            backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(2,active,textTopics,topicCount),width=5)
            backButton.grid(row = 6, column = 0, sticky=SW) 
            weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.updateRatingFrame(textTopics,topicCount-1,active,self.activeType.get()),width=5)
            weiterButton.grid(row = 6, column = 1, sticky=SW)
        elif active == 0:
            self.passiveType = IntVar()
            self.passiveType.set(defaultPassiveType)
            Label(self.rateBox,text="Strategie "+strategyNo).grid(row=0, column = 0,columnspan=2, sticky = W,pady=5)
            Label(self.rateBox,text="Locus of Control").grid(row=1, column = 0,columnspan=2, sticky = W,pady=5)
            Radiobutton(self.rateBox, text="sozial",variable=self.passiveType,value=0).grid(row = 2, column = 0,columnspan=2,sticky = W)
            Radiobutton(self.rateBox, text="fatalistisch",variable=self.passiveType,value=1).grid(row = 3, column = 0,columnspan=2,sticky = W)
            Radiobutton(self.rateBox, text="unklar",variable=self.passiveType,value=2).grid(row = 4, column = 0,columnspan=2,sticky = W)
            self.rateBox.rowconfigure(5, weight=1)
            backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(2,active,textTopics,topicCount),width=5)
            backButton.grid(row = 6, column = 0, sticky=SW)
            weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.updateRatingFrame(textTopics,topicCount-1,active,self.passiveType.get()),width=5)
            weiterButton.grid(row = 6, column = 1, sticky=SW)

    def rateText(self, value):
        data = {}
        data["ID"] = self.texts[self.cur][0]
        data["rateable"] = value
        data["identifyable"] = self.identVar.get()
        data["ideaCount"] = self.topicNumber.get()
        if data["ideaCount"] > 0:
            data["dontknow"] = -1
            data["zufrieden"] = -1
            data["resignation"] = -1
            data["weiterso"] = -1
            data["anderes"] = -1
        else:
            data["dontknow"] = self.dontknow.get()
            data["zufrieden"] = self.zufrieden.get()
            data["resignation"] = self.resignation.get()
            data["weiterso"] = self.weiterso.get()
            data["anderes"] = self.anderes.get()

        data["comment"] = self.comment.get("1.0",END).strip()
        
        self.ratingData[str(self.texts[self.cur][0])].update(data)
        #print(self.ratingData[str(data["ID"])])
 
        if self.cur+1==len(self.texts):
            showinfo('Fertig', 'Sie haben alle Texte bewertet')
            self.quit()
        else:
            self.cur += 1
        self.setText(True)
 
    def resume(self):
        filename = "../"+self.textField.get() + ".csv"  
        fromStart = True        
        if self.cur > 0:
            fromStart = False
        if os.path.isfile(filename):
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                next(reader, None)
                for row in reader:
                    data = {"ID":row[0],"rateable":int(row[1]),"identifyable":int(row[2]),
                    "ideaCount":int(row[3]),"dontknow":int(row[4]),"zufrieden":int(row[5]),"resignation":int(row[6]),
                    "weiterso":int(row[7]),"anderes":int(row[8]),
                    "active1":int(row[9]),"activeType1":int(row[10]),"passiveType1":int(row[11]),
                    "active2":int(row[12]),"activeType2":int(row[13]),"passiveType2":int(row[14]),
                    "active3":int(row[15]),"activeType3":int(row[16]),"passiveType3":int(row[17]),
                    "active4":int(row[18]),"activeType4":int(row[19]),"passiveType4":int(row[20]),
                    "active5":int(row[21]),"activeType5":int(row[22]),"passiveType5":int(row[23]),"comment":row[24]}
                    self.ratingData[row[0]] = data
                    if fromStart:
                        self.cur += 1
            #check if it is the last text
            if self.cur == len(self.texts):
                showinfo('Fertig', 'Sie haben alle Texte bewertet')
                self.quit()
            #print(self.ratingData)
            self.setText(True)

    def printData(self):
        filename = "../"+self.textField.get() + ".csv"
        if len(self.ratingData)>0:
            with open(filename, 'w', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter='\t',quotechar='"',quoting=csv.QUOTE_NONNUMERIC,)
                datawriter.writerow(["ID","rateable","identifyable",
                    "ideaCount","dontknow","zufrieden","resignation",
                    "weiterso","anderes","active1","activeType1","passiveType1",
                    "active2","activeType2","passiveType2",
                    "active3","activeType3","passiveType3",
                    "active4","activeType4","passiveType4",
                    "active5","activeType5","passiveType5","comment"])
               # print(self.ratingData)
                for key in self.ratingData:
                    data = self.ratingData[key]
                    #print(data)
                    #only print complete lines
                    if len(data) == 25:
                        datawriter.writerow([data["ID"],data["rateable"],data["identifyable"],
                                    data["ideaCount"],data["dontknow"],data["zufrieden"],
                                    data["resignation"],data["weiterso"],data["anderes"],
                                    data["active1"],data["activeType1"],data["passiveType1"],
                                    data["active2"],data["activeType2"],data["passiveType2"],
                                    data["active3"],data["activeType3"],data["passiveType3"],
                                    data["active4"],data["activeType4"],data["passiveType4"],
                                    data["active5"],data["activeType5"],data["passiveType5"],
                                    str(data["comment"])])

    def quit(self):
        self.printData()
        root.quit()

    #add previous data to buttons and fields
    def back(self, status, active, textTopics, topicCount):
        data = self.ratingData[str(self.texts[self.cur][0])]
        currentTopic = textTopics - topicCount +1
        #print(status)
        #setting former activity rating
        active = self.active
        if "active"+str(currentTopic-1) in data:
            if data["active"+str(currentTopic-1)] != -1:
                active = data["active"+str(currentTopic-1)]

        #initial decision, no of ideas
        #back: go back to löast decision
        if status == 0:
            if self.cur > 0:
                self.cur-=1
                self.setText(False)
                
        #decision about activity or zero ideas 
        #back: go back to no of ideas OR previous activity
        elif status == 1:
            if currentTopic > 1 :
                self.activeRating(active, textTopics, topicCount+1)
            else :
                self.setText(True)
        #decision about active/passive type OR rating of individual ideas
        #back: go to activity decision OR previous idea rating
        elif status == 2:
            #print("status"+str(status))
            self.updateRatingFrame(textTopics,topicCount,-1,-1)
                

    def setText(self,fromScratch):
        if fromScratch:
            self.makeRatingFrame()
        self.topicNumber.set(1)
        self.identVar.set(0)
        textlabel = Text(self, font = "Helvetica 14",wrap=WORD,height=8,width=70)
        textlabel.insert(END,self.texts[self.cur][1])
        textlabel.config(state=DISABLED)
        textlabel.grid(row=2, column=0, columnspan = 4, sticky = W)
        textPosition = 'Text: '+str(self.texts[self.cur][0]+" von "+str(len(self.texts)))
        textNumber = Label(self, text=textPosition, justify=LEFT)
        textNumber.grid(row = 1, column = 0, sticky=W)
        
        #key is known, data exists
        if str(self.texts[self.cur][0]) in self.ratingData:
            data = self.ratingData[str(self.texts[self.cur][0])]
            if len(data) == 25:
                self.identVar.set(data["identifyable"])
                self.comment.insert(END,data["comment"])
                self.topicNumber.set(data["ideaCount"])
                self.dontknow.set(data["dontknow"])
                self.zufrieden.set(data["zufrieden"])
                self.resignation.set(data["resignation"])
                self.weiterso.set(data["weiterso"])
                self.anderes.set(data["anderes"])
                if data["rateable"] == 0:
                    data["rateable"] = 1
                    fromScratch = True
                    self.makeRatingFrame()
                if self.topicNumber.get() > 0:
                    self.active.set(data["active"+str(self.topicNumber.get())])
                if not fromScratch:
                    if self.topicNumber.get() == 0:
                        self.updateRatingFrame(self.topicNumber.get(),self.topicNumber.get(),-1,-1)
                    else:
                        self.activeRating(self.active.get(), self.topicNumber.get(), 1)
            else:
                self.ratingData[str(self.texts[self.cur][0])] = {}
                data = {}
                for i in range(1,6):
                        data["active"+str(i)]=-1
                        data["activeType"+str(i)]=-1
                        data["passiveType"+str(i)]=-1
                data["dontknow"] = -1
                data["zufrieden"] = -1
                data["resignation"] = -1
                data["weiterso"] = -1
                data["anderes"] = -1
                self.ratingData[str(self.texts[self.cur][0])].update(data)
           # print("settext:")
           # print(data)
        else:
            self.ratingData[str(self.texts[self.cur][0])] = {}
            data = {}
            for i in range(1,6):
                    data["active"+str(i)]=-1
                    data["activeType"+str(i)]=-1
                    data["passiveType"+str(i)]=-1
            data["dontknow"] = -1
            data["zufrieden"] = -1
            data["resignation"] = -1
            data["weiterso"] = -1
            data["anderes"] = -1
            self.ratingData[str(self.texts[self.cur][0])].update(data)

    def onExit(self):
        self.quit()
 
def main():
    d = NameDialog(root,title = "Bitte Namen eingeben")
    rater = d.result
    ex = CodingWindow(root, rater)
    root.protocol("WM_DELETE_WINDOW", ex.onExit)      
    root.mainloop() 


if __name__ == '__main__':
    main()  
