import os
import sys
import random
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELAT ={
    pg.K_UP: (0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRct or 爆弾Rct
    戻り値:判定結果タプル(横方向,縦方向)
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
          kuro_img = pg.Surface((WIDTH,HEIGHT))  # 空のSurface
          pg.draw.rect(kuro_img,(0,0,0),(0,0,WIDTH,HEIGHT))  # 黒の四角を描画
          kuro_rct = kuro_img.get_rect()

          kuro_img.set_alpha(80)  # 透明

          kuro_rct.centerx = WIDTH/2  # 座標横
          kuro_rct.centery = HEIGHT/2  # 座標縦
          screen.blit(kuro_img,[0,0])  # 黒描画

            # 透明

          
          fonto = pg.font.Font(None, 80)  # gameover表示
          txt = fonto.render("Game Over", True, (255,255,255))
          kuro_img.blit(txt, [400,300])

          hidari_img = pg.image.load("fig/8.png")  # 画像   
          kuro_img.blit(hidari_img ,[100,100])
          #_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)

          screen.blit(kuro_img,[0,0])
          
          pg.display.update()
          time.sleep(5)
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img =pg.SurfaceType((20,20))  # 空のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  # 赤い爆弾円
    bb_img.set_colorkey((0,0,0))  # 四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()  # 爆弾rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標 
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key,mv in  DELAT.items():
            if key_lst[key]:
                sum_mv[0] +=mv[0] #  横方向の移動量加算
                sum_mv[1] +=mv[1] #  縦方向の移動量加算
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        if kk_rct.colliderect(bb_rct):  # こうかとん爆弾の衝突判定
            
            return gameover(screen) # ゲームオーバー
        
        bb_rct.move_ip(vx, vy)  # 爆弾移動
        yoko, tate =check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img,bb_rct)  # 爆弾描画
       # screen.blit(kuro_img,kuro_rct)
       
        pg.display.update()
        tmr += 1
        clock.tick(50)
       
        

       
          
         
       
        
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
