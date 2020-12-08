from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
		
    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockType = -1
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        self.line_index = 0#
        return

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self):  # To be implemented!!
        new_array = self.oScreen.get_array()
        array = self.oScreen.get_array()
        y = self.oScreen.get_dy()-Tetris.iScreenDw  #보드 y길이 - 버퍼 길이 = 실제 출력 y길이
        self.line_index = 0   #1로 꽉찬 줄의 높이index (꼭대기 = 0)
        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):#꼭대기층 부터 탐색
            cnt = 0 #각 칸에서 1의 개수 세기
            #모든 줄 체크하기
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):#실제 출력x축을 한번 훑기
                cnt += array[y][x]
                
            #꽉 찬 줄인지 확인
            if cnt == self.oScreen.get_dx()-2*Tetris.iScreenDw:
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
                self.line_index = y
                self.tempBlk = self.oScreen.clip(0, Tetris.iScreenDw, self.line_index, Tetris.iScreenDw + self.iScreenDx)
                self.oScreen.paste(self.tempBlk, 1, Tetris.iScreenDw)
        #return

    def accept(self, key): # To be implemented!!
        
        if key == 'a':
            self.left -= 1
            self.state = TetrisState.Running
        elif key == 'd':
            self.left += 1
            self.state = TetrisState.Running
        elif key == 's':
            self.top += 1
            self.state = TetrisState.Running
        elif key == 'w':
            self.idxBlockDegree += 1
            self.idxBlockDegree %= 4
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.state = TetrisState.Running
        elif key == ' ':
            while True:
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
                self.tempBlk = self.tempBlk + self.currBlk
                self.oScreen = Matrix(self.iScreen)
                self.oScreen.paste(self.tempBlk, self.top, self.left)#
                self.state = TetrisState.Running#
                
                if self.tempBlk.anyGreaterThan(1):
                    self.state = TetrisState.NewBlock
                    break
        elif key[0] == '0':
            if self.justStarted == True :
                self.justStarted = False
            else:
                print("\n\n\n\n")
                self.deleteFullLines()#
                self.iScreen = Matrix(self.oScreen)
            self.idxBlockType = int(key[1])
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx // 2 - 2
            self.idxBlockType = (1 + self.idxBlockType) % Tetris.nBlockTypes
            self.idxBlockDegree = 0
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]

            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk

            if self.tempBlk.anyGreaterThan(1):
                
                self.state = TetrisState.Finished
                self.oScreen = Matrix(self.iScreen)
                self.oScreen.paste(self.tempBlk, self.top, self.left)
                return self.state
            self.state = TetrisState.Running

        else :
            print("Wrong KEY!!")
            return self.state

        
        ### collision test-----------
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk
        if self.tempBlk.anyGreaterThan(1):
            if key == 'a':
                self.left += 1
            elif key == 'd':
                self.left -= 1
            elif key == 's':
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w':
                self.idxBlockDegree -= 1
                self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
                print("Impossible")
            elif key == ' ':
                self.top -= 1
                self.state = TetrisState.NewBlock


            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
        ###----------------------------


        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)
        

        return self.state

### end of class Tetris():
    
