import sys
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsScene, QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsItemGroup, QGraphicsView, QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QBrush, QPen, QColor, QTransform
from PySide6.QtCore import Qt, QPointF


#Commands to run this:
#1. None, already 

class ScratchWindow(QGraphicsScene):
    def __init__(self, parent):
        self.maxX = 500
        self.maxY = 500
        super().__init__(0, 0, self.maxX, self.maxY, parent)
        
        self.blackTheme = QColor(0, 0, 0, 255)
        self.brownTheme = QColor(126, 101, 81, 255)
        self.lightBrownTheme = QColor(147, 133, 129, 255)
        self.blueTheme = QColor(70, 99, 98, 255)
        self.blueGrayTheme = QColor(136, 150, 171, 255)
        self.lightBlueTheme = QColor(197, 213, 228, 255)

        self.activeLayerItem = None
        self.allLayers = list()

        # self.createLayerItem(0, 0, 200, 50, True, self.lightBlueTheme)
        self.createLayerItem(0, 0, 200, 50, True, self.lightBlueTheme)


        # brush = QBrush(lightBlueTheme)
        # pen = QPen(blackTheme)
        # pen.setWidth(5)

        # rect = QGraphicsRectItem(0, 0, 200, 50)
        # rect.setPos(50, 50)
        # rect.setBrush(brush)
        # rect.setPen(pen)

        # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # self.addItem(rect)
    
    def createLayerItem(self, locationX, locationY, dimX, dimY, isSample, brushColor):
        layerItem = LayerItem(locationX, locationY, dimX, dimY, self, isSample, brushColor)
        layerItem.setFocus(Qt.MouseFocusReason)
        self.addItem(layerItem)
        self.allLayers.append(layerItem)
    
    def removeLayerItem(self, layer):
        self.removeItem(layer)
        self.allLayers.pop(self.allLayers.index(self.activeLayerItem))
    
    # def createLayerItem(self, layerItem):
    #     self.addItem(layerItem)
    #     self.allLayers.append(layerItem)



class LayerItem(QGraphicsItemGroup):
    def __init__(self, locationX, locationY, dimX, dimY, parent : ScratchWindow, isSample, brushColor):
        super().__init__()

        #Functionality
        self.parent = parent
        self.isSample = isSample 
        self.dimX = dimX
        self.dimY = dimY
        self.before = None
        self.next = None
        self.oldLocation = QPointF(locationX, locationY)
        self.duplicateStuff = [locationX, locationY, dimX, dimY, parent, False, brushColor]

        if self.isSample == True:
            pass
        else:
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        #Looks
        piece1 = QGraphicsRectItem(locationX, locationY-10, 66, 10)
        piece1.setBrush(brushColor)
        piece1.setPen(brushColor)
        piece2 = QGraphicsRectItem(locationX+86, locationY-10, 114, 10)
        piece2.setBrush(brushColor)
        piece2.setPen(brushColor)
        piece3 = QGraphicsRectItem(locationX+66, locationY+dimY, 20, 10)
        piece3.setBrush(brushColor)
        piece3.setPen(brushColor)
        piece4 = QGraphicsRectItem(locationX, locationY, dimX, dimY)
        piece4.setBrush(brushColor)
        piece4.setPen(brushColor)

        self.addToGroup(piece1)
        self.addToGroup(piece2)
        self.addToGroup(piece3)
        self.addToGroup(piece4)

    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print("click")
        if event.button() == Qt.LeftButton:
            itemClicked = self
            print(self.pos())
            if self.isSample == False:
                self.oldLocation = self.pos()
                self.parent.activeLayerItem = itemClicked
                if self.before != None:
                    self.before.next = None
                    self.before = None
                print("clicked not a sample")
            elif self.isSample == True:
                self.parent.createLayerItem(self.duplicateStuff[0]+20, self.duplicateStuff[1]+20, self.duplicateStuff[2], 
                                            self.duplicateStuff[3], self.duplicateStuff[5], self.duplicateStuff[6])
            
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.parent.activeLayerItem != None: #Add connections or delete
            if self.parent.activeLayerItem.pos().x() < self.parent.maxX * 0.05:
                self.parent.removeLayerItem(self.parent.activeLayerItem)
                self.parent.activeLayerItem = None
            self.snapItem()
            self.move()
            self.parent.activeLayerItem = None
        super().mouseReleaseEvent(event)
    
    def snapItem(self):
        position = self.parent.activeLayerItem.pos()
        position.setY(position.y())
        connectingBlock = self.parent.itemAt(position+QPointF(50, 100), QTransform())
        if connectingBlock != None:
            print(":)")
        if connectingBlock != None and isinstance(connectingBlock, LayerItem) and connectingBlock.isSample == False:
            print("snap")
            self.before = connectingBlock
            connectingBlock.next = self
            position2 = QPointF()
            position2.setX(connectingBlock.pos().x())
            position2.setY(connectingBlock.pos().y()+self.dimY+15)
            self.setPos(position2)
                
    def move(self):
        currentItem = self
        difference = self.pos() - self.oldLocation
        while currentItem.next != None:
            currentItem = currentItem.next
            currentItem.setPos(currentItem.pos() + difference)

'''
class LayerItem(QGraphicsRectItem):
    def __init__(self, locationX, locationY, dimX, dimY, parent : ScratchWindow, isSample, brushColor):
        super().__init__(locationX, locationY, dimX, dimY)
        self.parent = parent
        self.isSample = isSample 
        self.dimX = dimX
        self.dimY = dimY
        self.before = None
        self.next = None
        self.oldLocation = QPointF(locationX, locationY)
        self.duplicateStuff = [locationX, locationY, dimX, dimY, parent, False, brushColor]

        self.setBrush(brushColor)
        self.setPen(brushColor)
        

        if self.isSample == True:
            pass
        else:
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            itemClicked = self
            if isinstance(itemClicked, LayerItem):
                if self.isSample == False:
                    self.oldLocation = self.pos()
                    self.parent.activeLayerItem = itemClicked
                    if self.before != None:
                        self.before.next = None
                        self.before = None
                    print("clicked not a sample")
                elif self.isSample == True:
                    self.parent.createLayerItem(self.duplicateStuff[0]+20, self.duplicateStuff[1]+20, self.duplicateStuff[2], 
                                                self.duplicateStuff[3], self.duplicateStuff[5], self.duplicateStuff[6])
            else:
                self.parent.activeLayerItem = None
            
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.parent.activeLayerItem != None: #Add connections or delete
            if self.parent.activeLayerItem.pos().x() < self.parent.maxX * 0.05:
                self.parent.removeLayerItem(self.parent.activeLayerItem)
            self.snapItem()
            self.move()
            self.parent.activeLayerItem = None
        super().mouseReleaseEvent(event)
    
    def snapItem(self):
        position = self.parent.activeLayerItem.pos()
        position.setY(position.y())
        connectingBlock = self.parent.itemAt(position, QTransform())
        if connectingBlock != None and isinstance(connectingBlock, LayerItem) and connectingBlock.isSample == False:
            print("snap")
            self.before = connectingBlock
            connectingBlock.next = self
            position2 = QPointF()
            position2.setX(connectingBlock.pos().x())
            position2.setY(connectingBlock.pos().y()+self.dimY+10)
            self.setPos(position2)
                
    def move(self):
        currentItem = self
        difference = self.pos() - self.oldLocation
        while currentItem.next != None:
            currentItem = currentItem.next
            currentItem.setPos(currentItem.pos() + difference)
'''

        
        

    