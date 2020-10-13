class queen:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def move(self):
        self.row += 1
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def conflict_queens(self,q):
        if(self.row == q.get_row() or self.col == q.get_col()):
            return True
        elif(abs(self.col-q.get_col())==abs(self.row-q.get_row())):
            return True
        return False