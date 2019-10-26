import pygame,random

pygame.init()
a=pygame.display.set_mode((600,760))
pygame.display.set_caption('Tetris')

def write(text,color,pos,size=75):
    font = pygame.font.Font(None, size)
    pos=list(pos)
    txt=font.render(text,False,color)
    if pos[0]==None:
        pos[0]=(600-txt.get_width())//2
    a.blit(txt,pos)

def button(text,rect,txt_pos,bg,txt_color,active_bg,active_txt_color,events):
    x,y=pygame.mouse.get_pos()
    pygame.draw.rect(a, bg, rect)
    write(text, txt_color, txt_pos)
    if rect[0]<x<rect[0]+rect[2] and rect[1]<y<rect[1]+rect[3]:
        pygame.draw.rect(a,active_bg,rect)
        write(text,active_txt_color,txt_pos)
        for event in events:
            if event.type==pygame.MOUSEBUTTONDOWN:return True
    return False

figures=(
    (((0,-1),(0,0),(0,1),(0,2)),((-1,0),(0,0),(1,0),(2,0)),),
    (((0,-1),(1,-1),(0,0),(0,1)),((-1,0),(0,0),(1,0),(1,1)),((0,1),(1,1),(1,0),(1,-1)),((-1,1),(0,1),(1,1),(-1,0))),
    (((0,0),(0,1),(1,0),(1,1)),),
    (((-1,0),(0,0),(1,0),(0,1)),((1,-1),(1,0),(1,1),(0,0)),((0,0),(-1,1),(0,1),(1,1)),((0,-1),(0,0),(0,1),(1,0))),
    (((-1,0),(0,0),(0,1),(1,1)),((1,-1),(1,0),(0,0),(0,1)))
)
q=0

while True:
    while q==0:
        a.fill((0,0,0))
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                exit()
        if button('PLAY',(200,300,200,100),(230,330),(255,255,255),(0,0,0),(180,180,180),(80,80,80),events):
            q=1
        pygame.display.update()
    now = random.choice(figures)
    s=random.randint(0,len(now)-1)
    pos=[14,-3]
    bricks=[0]*30
    for i in range(30):bricks[i]=[0]*45
    color=(random.randint(50,255),random.randint(50,255),random.randint(50,255))
    k=0
    l=75
    score=0
    while q==1:
        a.fill((0,0,0))
        events = pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    pos[0]+=1
                    for i in now[s]:
                        if i[0]+pos[0]>29:
                            pos[0]-=1
                            break
                        for j in bricks:
                            if bricks[i[0]+pos[0]][i[1]+pos[1]]!=0:
                                pos[0]-=1
                                break
                if event.key==pygame.K_LEFT:
                    pos[0]-=1
                    for i in now[s]:
                        if i[0]+pos[0]<0:
                            pos[0]+=1
                            break
                        if bricks[i[0]+pos[0]][i[1]+pos[1]]!=0:
                            pos[0]+=1
                            break
                if event.key==pygame.K_DOWN:
                    l=2
                    k=0
                if event.key==pygame.K_SPACE:
                    s=(s+1)%len(now)
        for i in range(len(bricks)):
            for m in range(len(bricks[i])):
                if bricks[i][m]!=0:
                    pygame.draw.rect(a,bricks[i][m],(i*20,m*20,19,19))
        for i in now[s]:
            pygame.draw.rect(a,color,((i[0]+pos[0])*20,(i[1]+pos[1])*20,19,19))
        pos[1]+=k//l
        k%=l
        k+=1
        for i in now[s]:
            if i[1]+pos[1]>36 or bricks[i[0]+pos[0]][i[1]+pos[1]+1]!=0:
                for j in now[s]:
                    bricks[j[0]+pos[0]][j[1]+pos[1]]=color
                score+=len(now[s])
                now = random.choice(figures)
                pos = [14, -4]
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                l=75
                s = random.randint(0, len(now) - 1)
            true=True
            while true:
                true=False
                for m in range(44,-1,-1):
                    sum=0
                    for cvb in range(0,30):
                        if bricks[cvb][m]!=0:sum+=1
                    if sum==30:
                        for cvb in range(30):
                            bricks[cvb][m]=0
                            for bn in range(30):
                                for nb in range(m-1,-1,-1):
                                    if bricks[bn][nb+1]==0:
                                        bricks[bn][nb + 1]=bricks[bn][nb]
                                        bricks[bn][nb]=0
                        true=True
        write('score:'+str(score),(255,255,255),(0,0),25)
        for i in bricks:
            if i[0]!=0:q=2
        pygame.display.update()
    for i in range(len(bricks)):
        for m in range(len(bricks[i])):
            if bricks[i][m] != 0:
                pygame.draw.rect(a, bricks[i][m], (i * 20, m * 20, 19, 19))
    write('score:' + str(score), (255, 255, 255), (None, 330))
    while q==2:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    q=0
            if event.type==pygame.QUIT:
                exit()