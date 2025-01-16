#-----------------------------------------------------------------
# title: pymunk_de_smartball
# author: sanbunnoichi
# desc: Smartball simulator
# site: https://github.com/sanbunno-ichi/pymunk_de_smartball
# license: MIT
# version: 1.0
#
#更新履歴
#2025.01.16 公開
#2025.01.10 作成開始
#-----------------------------------------------------------------
#PERFECTを目指してください
#ゲームの目的：より少ないボール数で到達することを目指す
#-----------------------------------------------------------------
import pyxel

SCREEN_WIDTH = 180
SCREEN_HEIGHT = 256
BALL_RADIUS = 5
BALLIN_RADIUS = 4
BALL_MAX = 20

#打ち出す力算出
#power : 200 = x : 63
#x = (power * 63)/200
PULL_PARAM = 40		#63(FULL)
ADD_POWER_MAX = 200		#シューター引っ張る力最大値
ADD_POWER_MIN = 36		#シューター引っ張る力最低値

#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x400
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理(RAM領域)

game_adv			=	WORK_TOP+0x00		#game_control number

G_TITLE				=	0
G_DEMOPLAY			=	1
G_GAME				=	2
G_SETTING			=	3
G_END				=	4
G_FIELD_CHANGE		=	5

game_subadv			=	WORK_TOP+0x01		#game_control sub-number

GS_INIT				=	0
GS_MAIN				=	1	#G_GAME
GS_PERFECT			=	2

board_number		=	WORK_TOP+0x02
wait_counter		=	WORK_TOP+0x03

hole_switch			=	WORK_TOP+0x10

B_HOLE00 = 0x0001
B_HOLE01 = 0x0002
B_HOLE02 = 0x0004
B_HOLE03 = 0x0008
B_HOLE04 = 0x0010
B_HOLE05 = 0x0020
B_HOLE06 = 0x0040
B_HOLE07 = 0x0080
B_HOLE08 = 0x0100
B_HOLE09 = 0x0200
B_HOLE10 = 0x0400
B_HOLE11 = 0x0800
B_HOLE12 = 0x1000
B_HOLE13 = 0x2000
B_HOLE14 = 0x4000
B_HOLE15 = 0x8000

shooter_gate_switch	=	WORK_TOP+0x11
B_GATE_CLOSE = 0x01		#シューターバンパーに当たった時にセットされる
B_GATE_CLOSED = 0x02	#閉じた状態
B_GATE_OPEN = 0x04		#玉打ち出し時にゲートオープン命令を出す

shooter_ball		=	WORK_TOP+0x12	#シューターにいるボールの番号をセット
shooter_power		=	WORK_TOP+0x13	#シューター引っ張る力
shooter_power_set	=	WORK_TOP+0x14
ball_type			=	WORK_TOP+0x15
ball_count			=	WORK_TOP+0x16


holein_ball			=	WORK_TOP+0x20		#hole_pos_tbl個数(15)：最大１６個、ホールに入ったボール番号を記憶
hole_pic_switch		=	WORK_TOP+0x30		#hole_pic_tbl個数(10)：最大１６個

ball_switch			=	WORK_TOP+0x100		#ボール複数化

BALLSW_READY	=	0x01		#シューターにセットされた
BALLSW_SHOT		=	0x02		#射出した
BALLSW_HOLEIN	=	0x04		#ホールイン
BALLSW_OUT		=	0x08		#フレームアウト

BALLSW_DEAD		=	0x40		#一旦body削除
BALLSW_STANDBY	=	0x80		#スタンバイ状態


hollin_pos			=	WORK_TOP+0x200		#ホールインしたボールの座標保存

#[S1]穴座標
hole_pos_tbl = [
	 56,  80,
	108,  80,
	 35, 105,
	 82, 105,
	129, 105,
	 56, 130,
	108, 130,
	 35, 156,
	 82, 156,
	129, 156,
	 56, 182,
	108, 182,
	 35, 203,
	 82, 203,
	129, 203,
	]

#[S1]ホール組み合わせセット
hole_pic_tbl = [
	0,1,6,5,		#0	box
	5,6,11,10,		#1	box
	2,3,8,7,		#2	box
	3,4,9,8,		#3	box
	0,3,6,9,		#4	naname line
	1,3,5,7,		#5	naname line
	2,5,8,11,		#6	naname line
	4,6,8,10,		#7	naname line
	12,13,14,-1,	#8	yoko line
	]

#[S1]軸座標
shaft_pos_tbl = [
	 42, 70,
	 56, 70,
	 70, 70,
	 82, 70,
	 94, 70,
	108, 70,
	120, 70,
	 29, 95,
	 41, 95,
	 76, 95,
	 88, 95,
	123, 95,
	135, 95,
	 42,120,
	 56,120,
	 70,120,
	 94,120,
	108,120,
	120,120,
	 12,128,
	152,128,
	 29,145,
	 41,145,
	 76,145,
	 88,145,
	123,145,
	135,145,
	 27,182,
	 50,170,
	 62,170,
	102,170,
	114,170,
	137,182,
	 12,200,
	 76,191,
	 88,191,
	152,200,
	]

#DEFAULT COLOR
defcol_tbl = [
	0x000000,
	0x2b335f,
	0x7e2072,
	0x19959c,
	0x8b4852,
	0x395c98,
	0xa9c1ff,
	0xeeeeee,
	0xd4186c,
	0xd38441,
	0xe9c35b,
	0x70c6a9,
	0x7696de,
	0xa3a3a3,
	0xff9798,
	0xedc7b0,
	]

class App:
	#-----------------------------------------------------------------
	#初期化
	#-----------------------------------------------------------------
	def __init__( self, pymunk, fps=60 ):
		self.pymunk = pymunk
		self.fps = fps
		pyxel.init( SCREEN_WIDTH, SCREEN_HEIGHT, fps=fps, title="pymunk_de_smartball" )
		pyxel.load("pinball.pyxres")
		self.work_clear()
		GWK[game_adv] = G_GAME
		GWK[game_subadv] = GS_INIT
		self.create_world()
		pyxel.camera(0, 0)
		pyxel.run(self.update, self.draw)

	#-----------------------------------------------------------------
	#効果音セット
	#-----------------------------------------------------------------
	def se_set(self,_number):
			pyxel.play( 3,_number )

	#-----------------------------------------------------------------
	#ワーク初期化
	#-----------------------------------------------------------------
	def work_clear(self):
		for _cnt in range( WORK_TOP, WORK_END ):
			GWK[_cnt] = 0

	def work_clear2(self):
		for _cnt in range( WORK_TOP+0x10, WORK_END ):
			GWK[_cnt] = 0


	#-----------------------------------------------------------------
	#ホールイン制御
	#-----------------------------------------------------------------
	def holein_control(self):
		hole_size = len(hole_pos_tbl)//2
		for _hcnt in range(hole_size):
			_bit = 1 << _hcnt
			#ホールにボールは入っていない
			if( ( GWK[hole_switch] & _bit ) == 0 ):
				#現在移動中のボールとのヒットチェックを行う
				for _bcnt in range(BALL_MAX):
					if( GWK[ball_switch+_bcnt] == 0 ):		#移動中
						#当たり判定

						#shapes_collide:衝突があれば衝突箇所の座標がリストで返ってきて、無ければ空のリストを返します。
						#class pymunk.ContactPointSet(normal: Vec2d, points: List[ContactPoint])[source]
						#cp : List[ContactPoint]
						#class pymunk.ContactPoint(point_a: Vec2d, point_b: Vec2d, distance: float)[source]
						if( self.hole_shape[_hcnt].shapes_collide( self.ball_shape[_bcnt] ).points ):
							#B_HOLExxをセット
							GWK[hole_switch] |= _bit
							#どのボールがこのホールにインしたかを保存
							GWK[holein_ball + _hcnt] = _bcnt

							#ホールインしたボールをセット
							x, y = self.hole_body[_hcnt].position
							self.ball_body[_bcnt].position = x, y
							#ボールの速度をリセット
							self.ball_body[_bcnt].velocity = (0, 0)
							#ボール挙動を停止
							self.ball_body[_bcnt].sleep()
							
							#ホールインしたボールの座標を保存
							GWK[hollin_pos + ( _bcnt * 3 + 0 )] = x
							GWK[hollin_pos + ( _bcnt * 3 + 1 )] = y
							GWK[hollin_pos + ( _bcnt * 3 + 2 )] = self.ball_body[_bcnt].angle

							#ホールインセット
							GWK[ball_switch + _bcnt] |= BALLSW_HOLEIN
							GWK[shooter_ball] = -1
							self.se_set(4)
							break

		#ホールインしたボールがhole_pic_tblで揃ってるかどうかをチェックする
		hole_pic_size = len(hole_pic_tbl)//4
		for _cnt in range(hole_pic_size):
			#未チェック
			if( GWK[hole_pic_switch + _cnt] == 0 ):
				#組み合わせのホールが埋まっているかのチェック
				_check_switch = 0
				for _num in range(4):
					_bitcnt = hole_pic_tbl[_cnt * 4 + _num]
					if( _bitcnt != (-1) ):
						_bit = 1 << _bitcnt
						_check_switch |= _bit
				
				if( ( GWK[hole_switch] & _check_switch ) == _check_switch ):
					#揃ってます
					GWK[hole_pic_switch + _cnt] = 1
					self.se_set(32)


	#-----------------------------------------------------------------
	#シューターゲート通過チェック
	#-----------------------------------------------------------------
	def shooter_gate_control(self):
		if( GWK[shooter_gate_switch] == 0 ):
			#現在移動中のボールとのヒットチェックを行う
			for _bcnt in range(BALL_MAX):
				#移動中の時
				if( GWK[ball_switch+_bcnt] == 0 ):
					x,y = self.ball_body[_bcnt].position
					if( y < 75 ):
						#シューターゲート通過した時シューターゲートを閉じる
						GWK[shooter_gate_switch] |= B_GATE_CLOSE
						#self.se_set(5)

	#-----------------------------------------------------------------
	#ゲートコントロール（開閉（add/remove））制御
	#後始末で使うので関数分けしておく
	#-----------------------------------------------------------------
	def gate_control(self):
		#シューターゲートスイッチが入ったらゲートを閉じる
		if( ( ( GWK[shooter_gate_switch] & B_GATE_CLOSED ) == 0 ) and
			( GWK[shooter_gate_switch] & B_GATE_CLOSE ) ):		#CLOSE命令
			self.space.add(self.shooter_gate_body, self.shooter_gate_shape)
			GWK[shooter_gate_switch] |= B_GATE_CLOSED

		elif( ( GWK[shooter_gate_switch] & ( B_GATE_CLOSED + B_GATE_OPEN ) ) == ( B_GATE_CLOSED + B_GATE_OPEN ) ):	#OPEN命令
			self.space.remove(self.shooter_gate_body, self.shooter_gate_shape)
			GWK[shooter_gate_switch] = 0

	#-----------------------------------------------------------------
	#create_world
	#	ホールは１５個、軸３５本
	#	シューター、シューターゲート、ストッパーバンパー
	#-----------------------------------------------------------------
	def create_world(self):
		from pymunk import Vec2d

		self.space = self.pymunk.Space()
		self.space.gravity = ( 0.0, 150.0 )		#台の傾斜（重力）
		self.space.sleep_time_threshold = 0.3

		#外壁
		static_lines = [
			self.pymunk.Segment(self.space.static_body, (  70, 255), (   7, 206), 1.0),
			self.pymunk.Segment(self.space.static_body, (   7, 206), (   7,  93), 1.0),
			self.pymunk.Segment(self.space.static_body, (   7,  93), (  12,  83), 1.0),
			self.pymunk.Segment(self.space.static_body, (  12,  83), (  20,  71), 1.0),
			self.pymunk.Segment(self.space.static_body, (  20,  71), (  22,  67), 1.0),
			self.pymunk.Segment(self.space.static_body, (  22,  67), (  17,  57), 1.0),
			self.pymunk.Segment(self.space.static_body, (  17,  57), (  23,  47), 1.0),
			self.pymunk.Segment(self.space.static_body, (  23,  47), (  32,  38), 1.0),
			self.pymunk.Segment(self.space.static_body, (  32,  38), (  42,  31), 1.0),
			self.pymunk.Segment(self.space.static_body, (  42,  31), (  56,  25), 1.0),
			self.pymunk.Segment(self.space.static_body, (  56,  25), (  72,  21), 1.0),
			self.pymunk.Segment(self.space.static_body, (  72,  21), (  86,  20), 1.0),
			self.pymunk.Segment(self.space.static_body, (  86,  20), ( 104,  21), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 104,  21), ( 120,  24), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 120,  24), ( 134,  29), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 134,  29), ( 145,  35), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 145,  35), ( 153,  43), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 153,  43), ( 158,  48), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 158,  48), ( 163,  55), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 163,  55), ( 168,  63), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 168,  63), ( 173,  78), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173,  78), ( 173, 145), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173, 145), ( 173, 249), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 173, 249), ( 161, 249), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 161, 249), ( 161, 145), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 161, 145), ( 161,  90), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 161,  90), ( 159,  87), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 159,  87), ( 157,  90), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 157,  90), ( 157, 206), 1.0),
			self.pymunk.Segment(self.space.static_body, ( 157, 206), (  94, 255), 1.0),
		]
		for line in static_lines:
			line.elasticity = 0.7
			line.friction = 0.3
			line.group = 1
		#外壁を物理空間に追加
		self.space.add(*static_lines)
		
		#シューター
		self.shooter_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.shooter_body.position = 167, 180
		self.shooter_shape = self.pymunk.Segment(self.shooter_body, Vec2d(-6, 0), Vec2d(6, 0), 1)
		#反射係数（弾性）を設定
		self.shooter_shape.elasticity = 0.4
		#摩擦係数を設定
		self.shooter_shape.friction = 0.3
		self.space.add(self.shooter_body, self.shooter_shape)

		#ボール生成
		self.ball_body = [0 for tbl in range(BALL_MAX)]
		self.ball_shape = [0 for tbl in range(BALL_MAX)]

		#ホール設定
		hole_size = len(hole_pos_tbl)//2
		self.hole_body = [0 for tbl in range(hole_size)]
		self.hole_shape = [0 for tbl in range(hole_size)]
		for _cnt in range(hole_size):
			self.hole_body[_cnt] = self.pymunk.Body( body_type=self.pymunk.Body.STATIC )
			self.hole_body[_cnt].position = hole_pos_tbl[_cnt*2+0], hole_pos_tbl[_cnt*2+1]
			self.hole_shape[_cnt] = self.pymunk.Circle(self.hole_body[_cnt], 2)		#ホールの大きさを小さく（元は6）
			self.space.add(self.hole_body[_cnt], self.hole_shape[_cnt])

		#シューターゲート
		self.shooter_gate_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.shooter_gate_body.position = 159, 87
		self.shooter_gate_shape = self.pymunk.Segment(self.shooter_gate_body, Vec2d(0, 0), Vec2d(14, -9), 2)
		self.shooter_gate_shape.elasticity = 2.0
		#最初は「開け」状態にしておく
		#self.space.add(self.shooter_gate_body, self.shooter_gate_shape)
		GWK[shooter_gate_switch] = 0

		#ストップバンパー
		self.bumper_body = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
		self.bumper_body.position = (21, 63)
		self.bumper_shape = self.pymunk.Circle( self.bumper_body, 5 )
		self.bumper_shape.elasticity = 1.0
		self.bumper_shape.friction = 0.3
		self.space.add(self.bumper_body, self.bumper_shape)

		#軸
		shaft_size = len(shaft_pos_tbl)//2
		self.shaft_body = [0 for tbl in range(shaft_size)]
		for _cnt in range(shaft_size):
			self.shaft_body[_cnt] = self.pymunk.Body(body_type=self.pymunk.Body.STATIC)
			self.shaft_body[_cnt].position = shaft_pos_tbl[_cnt*2+0], shaft_pos_tbl[_cnt*2+1]-2		#[-2]暫定
			self.circle = self.pymunk.Circle(self.shaft_body[_cnt], 1)
			self.circle.elasticity = 0.7
			self.circle.friction = 0.3
			self.space.add(self.shaft_body[_cnt], self.circle)


	#-----------------------------------------------------------------
	#ボール生成
	#-----------------------------------------------------------------
	def ball_create( self, _num ):
		if( BALL_MAX > _num ):
			#space内にすでに登録済みか確認
			for b in self.space.bodies:
				if( b == self.ball_body[_num] ):
					print("[ball_create ERROR]ALREADY SET END _num=", _num)
					return

			mass = 100
			r = BALL_RADIUS
			moment = self.pymunk.moment_for_circle(mass, 0, r, (0, 0))
			self.ball_body[_num] = self.pymunk.Body(mass, moment)
			self.ball_body[_num].position = ( 167, 180-6 )

			self.ball_shape[_num] = pymunk.Circle(self.ball_body[_num], r, (0, 0))
			#反射係数（弾性）を設定
			self.ball_shape[_num].elasticity = 0.4
			#摩擦係数を設定
			self.ball_shape[_num].friction = 0.3
			self.space.add(self.ball_body[_num], self.ball_shape[_num])

	#-----------------------------------------------------------------
	#更新
	#-----------------------------------------------------------------
	def update(self):
		from pymunk import Vec2d
		if( GWK[game_adv] == G_GAME ):
			if( GWK[game_subadv] == GS_INIT ):

				#ゲーム内パラメータクリア
				self.work_clear2()

				#有効ボール番号初期化
				GWK[shooter_ball] = -1

				#ボール状態初期化
				for _cnt in range(BALL_MAX):
					GWK[ball_switch + _cnt] = BALLSW_DEAD

				GWK[game_subadv] = GS_MAIN

			elif( GWK[game_subadv] == GS_MAIN ):

				step = 5  # Run multiple steps for more stable simulation
				step_dt = 1 / self.fps / step
				for _ in range(step):
					self.space.step(step_dt)

				#操作
				if self.getInputB():
					pyxel.quit()

				#裏技（一発目打つ前に押下するとボール種別が変わります（３種類））
				if self.getInputY():
					if( GWK[ball_count] == 1 ):
						GWK[ball_type] += 1
						if( GWK[ball_type] > 1 ):
							GWK[ball_type] = 0
							
				#ボール番号は有効？
				if( GWK[shooter_ball] == (-1) ):
					#無効なら次のボール準備
					for _cnt in range(BALL_MAX):
						if( GWK[ball_switch + _cnt] == BALLSW_DEAD ):
							self.ball_create(_cnt)
							GWK[ball_switch + _cnt] = 0
							GWK[shooter_ball] = _cnt
							GWK[ball_count] += 1
							break

				else:
					#ボール番号を取得
					setnum = GWK[shooter_ball]
					#有効？
					if( setnum >= 0 ):

						#A押下でシューターを引っ張り（0x02 set）、A離してショットON（0x03 set is shoot）
						if self.getPushA():
							GWK[shooter_power] += 1
							if( GWK[shooter_power] > ADD_POWER_MAX ):
								#上限値設定
								GWK[shooter_power] = ADD_POWER_MAX

							if( ( GWK[ball_switch + setnum] & (BALLSW_READY+BALLSW_SHOT) ) == BALLSW_READY ):
								if( GWK[shooter_gate_switch] & B_GATE_CLOSED ):
									GWK[shooter_gate_switch] |= B_GATE_OPEN		#シューターゲートを開く
								GWK[ball_switch + setnum] |= BALLSW_SHOT

						else:
							if( ( GWK[ball_switch + setnum] & (BALLSW_READY+BALLSW_SHOT) ) == (BALLSW_READY+BALLSW_SHOT) ):
								#ボールショット
								GWK[ball_switch + setnum] &= ~(BALLSW_READY+BALLSW_SHOT)
								#射出したボール状態は"0"になる

								GWK[shooter_power_set] = GWK[shooter_power]
								GWK[shooter_power] = 0

								#ボールに与える力に変換
								if( GWK[shooter_power_set] < ADD_POWER_MIN ):
									#最低限シューターから排出される力をセットする
									GWK[shooter_power_set] = ADD_POWER_MIN
								add_power = ( GWK[shooter_power_set] * 500 ) * ( -1 )
								self.ball_body[setnum].apply_impulse_at_local_point((0, add_power), (0, 0))
								self.se_set(16)
								
							else:
								GWK[shooter_power] = 0


						#ボールが止まったかどうかを確認
						if( abs( self.ball_body[setnum].velocity.y ) < 0.0001 ):
							#シューター上の時
							if( ( self.ball_body[setnum].position.x >= 166 ) and 
								( self.ball_body[setnum].position.x <= 168 ) ):
								if( GWK[ball_switch + setnum] == 0 ):
									#ボールの速度をリセット
									self.ball_body[setnum].velocity = Vec2d(0, 0)
									#再度射出待ちに設定
									GWK[ball_switch + setnum] |= BALLSW_READY
									GWK[shooter_ball] = setnum

							#ボード上の時
							else:
								#ちょっとだけ動かす
								if( pyxel.frame_count & 0x01 ):
									self.ball_body[setnum].apply_impulse_at_local_point((100, 0), (0, 0))
								else:
									self.ball_body[setnum].apply_impulse_at_local_point((-100, 0), (0, 0))

					#シューターを引っ張る力に合わせて移動させる
					shooter_y = (180 + GWK[shooter_power] * PULL_PARAM / ADD_POWER_MAX)
					self.shooter_body.position = 167, shooter_y

				#ボールが画面外になったかどうかの判定
				for _cnt in range(BALL_MAX):
					#SHOT済み、かつ、ホールインしてない、かつ、remove以外時にチェックする
					if( ( GWK[ball_switch + _cnt] & (BALLSW_READY+BALLSW_SHOT+BALLSW_HOLEIN+BALLSW_DEAD) ) == 0 ):
						if( self.ball_body[_cnt].position.get_distance((SCREEN_WIDTH//2, 256)) > 320 ):
							GWK[ball_switch + _cnt] = BALLSW_DEAD
							self.space.remove(self.ball_body[_cnt], self.ball_shape[_cnt])
							GWK[shooter_ball] = -1
							self.se_set(29)


				#ホールイン制御
				self.holein_control()
				#シューターゲート制御
				self.shooter_gate_control()
				#ゲート制御
				self.gate_control()

			#パーフェクト後
			elif( GWK[game_subadv] == GS_PERFECT ):
				#リトライ開始
				if self.getInputA():

					#ホールインボール後始末
					hole_size = len(hole_pos_tbl)//2
					for _hcnt in range(hole_size):
						_bit = 1 << _hcnt
						if( GWK[hole_switch] & _bit ):
							_bcnt = GWK[holein_ball + _hcnt]
							#space内にすでに登録済みか確認
							for b in self.space.bodies:
								if( b == self.ball_body[_bcnt] ):
									#存在してたので削除
									self.space.remove( self.ball_body[_bcnt], self.ball_shape[_bcnt] )
									GWK[hole_switch] &= ~_bit
									break
						GWK[holein_ball + _hcnt] = 0
						GWK[hollin_pos + ( _hcnt * 3 + 0)] = 0
						GWK[hollin_pos + ( _hcnt * 3 + 1)] = 0
						GWK[hollin_pos + ( _hcnt * 3 + 2)] = 0

					if( GWK[hole_switch] != 0 ):
						print("[ERROR]まだボール残ってます：",hex(GWK[hole_switch]))
						#残るはずはないのだけれど・・・一応ログ出してみる

					#組み合わせスイッチクリア
					for _cnt in range(16):
						GWK[hole_pic_switch + _cnt] = 0

					#シューターゲート後始末
					if( GWK[shooter_gate_switch] & B_GATE_CLOSED ):
						GWK[shooter_gate_switch] |= B_GATE_OPEN		#シューターゲートを開く
					#ゲート制御
					self.gate_control()
					
					#リトライ実行
					GWK[game_subadv] = GS_INIT

	#-----------------------------------------------------------------
	#res table
	#-----------------------------------------------------------------
	IDMAX = 0x21
	ctbl = [
		# u,    v,    us,   vs
		[ 0x34, 0x00, 0x03, 0x05 ],		#0x00 小黄軸
		[ 0x40, 0x00, 0x0a, 0x0a ],		#0x01 青ボール回転16パターン
		[ 0x50, 0x00, 0x0a, 0x0a ],		#0x02
		[ 0x60, 0x00, 0x0a, 0x0a ],		#0x03
		[ 0x70, 0x00, 0x0a, 0x0a ],		#0x04
		[ 0x40, 0x10, 0x0a, 0x0a ],		#0x05
		[ 0x50, 0x10, 0x0a, 0x0a ],		#0x06
		[ 0x60, 0x10, 0x0a, 0x0a ],		#0x07
		[ 0x70, 0x10, 0x0a, 0x0a ],		#0x08
		[ 0x40, 0x20, 0x0a, 0x0a ],		#0x09
		[ 0x50, 0x20, 0x0a, 0x0a ],		#0x0a
		[ 0x60, 0x20, 0x0a, 0x0a ],		#0x0b
		[ 0x70, 0x20, 0x0a, 0x0a ],		#0x0c
		[ 0x40, 0x30, 0x0a, 0x0a ],		#0x0d
		[ 0x50, 0x30, 0x0a, 0x0a ],		#0x0e
		[ 0x60, 0x30, 0x0a, 0x0a ],		#0x0f
		[ 0x70, 0x30, 0x0a, 0x0a ],		#0x10
		[ 0x40, 0x40, 0x0a, 0x0a ],		#0x11 赤ボール回転16パターン
		[ 0x50, 0x40, 0x0a, 0x0a ],		#0x12
		[ 0x60, 0x40, 0x0a, 0x0a ],		#0x13
		[ 0x70, 0x40, 0x0a, 0x0a ],		#0x14
		[ 0x40, 0x50, 0x0a, 0x0a ],		#0x15
		[ 0x50, 0x50, 0x0a, 0x0a ],		#0x16
		[ 0x60, 0x50, 0x0a, 0x0a ],		#0x17
		[ 0x70, 0x50, 0x0a, 0x0a ],		#0x18
		[ 0x40, 0x60, 0x0a, 0x0a ],		#0x19
		[ 0x50, 0x60, 0x0a, 0x0a ],		#0x1a
		[ 0x60, 0x60, 0x0a, 0x0a ],		#0x1b
		[ 0x70, 0x60, 0x0a, 0x0a ],		#0x1c
		[ 0x40, 0x70, 0x0a, 0x0a ],		#0x1d
		[ 0x50, 0x70, 0x0a, 0x0a ],		#0x1e
		[ 0x60, 0x70, 0x0a, 0x0a ],		#0x1f
		[ 0x70, 0x70, 0x0a, 0x0a ],		#0x20
	]

	#-----------------------------------------------------------------
	#キャラクタセット
	#	X座標, Y座標, id番号
	#-----------------------------------------------------------------
	def cput(self, _xp, _yp, _id ):
		if( _id < self.IDMAX ):
			pyxel.blt( _xp, _yp, 0, self.ctbl[_id][0], self.ctbl[_id][1], self.ctbl[_id][2], self.ctbl[_id][3], 0 )

	#-----------------------------------------------------------------
	#描画
	#-----------------------------------------------------------------
	def draw(self):
		import numpy as np

		pyxel.cls(0)
		
		pyxel.text( (SCREEN_WIDTH//2 - (4*19//2)) , 10, 'S M A R T  B A L L', 7 )
		pyxel.text( 120, 240, 'BALL:', 7 )
		pyxel.text( 140, 240, str(GWK[ball_count]-1), 7 )

		#操作説明
		if( ( GWK[game_adv] == G_GAME ) and ( GWK[game_subadv] == GS_MAIN ) ):
			pyxel.text( (SCREEN_WIDTH//2 - (4*28//2)) , 40, 'Z-KEY OR A-BUTTON PUSH START', 10 )
			pyxel.text( (SCREEN_WIDTH//2 - (4*32//2)) , 40+8, 'SELECT THE FOECE YOU WANT TO HIT', 10 )
			pyxel.text( (SCREEN_WIDTH//2 - (4*32//2)) , 40+16, 'AND RELEASE THE BUTTON TO SHOOT.', 10 )
		elif( ( GWK[game_adv] == G_GAME ) and ( GWK[game_subadv] == GS_PERFECT ) ):
			pyxel.text( (SCREEN_WIDTH//2 - (4*25//2)) , 40+4, '!!!! P E R F E C T !!!!', 10 )
			pyxel.text( (SCREEN_WIDTH//2 - (4*28//2)) , 40+12, 'Z-KEY OR A-BUTTON IS RETRY', 10 )


		#外壁
		pyxel.line(  70, 255,   7, 206, 7 )
		pyxel.line(   7, 206,   7,  93, 7 )
		pyxel.line(   7,  93,  12,  83, 7 )
		pyxel.line(  12,  83,  20,  71, 7 )
		pyxel.line(  20,  71,  22,  67, 7 )
		pyxel.line(  22,  67,  17,  57, 7 )
		pyxel.line(  17,  57,  23,  47, 7 )
		pyxel.line(  23,  47,  32,  38, 7 )
		pyxel.line(  32,  38,  42,  31, 7 )
		pyxel.line(  42,  31,  56,  25, 7 )
		pyxel.line(  56,  25,  72,  21, 7 )
		pyxel.line(  72,  21,  86,  20, 7 )
		pyxel.line(  86,  20, 104,  21, 7 )
		pyxel.line( 104,  21, 120,  24, 7 )
		pyxel.line( 120,  24, 134,  29, 7 )
		pyxel.line( 134,  29, 145,  35, 7 )
		pyxel.line( 145,  35, 153,  43, 7 )
		pyxel.line( 153,  43, 158,  48, 7 )
		pyxel.line( 158,  48, 163,  55, 7 )
		pyxel.line( 163,  55, 168,  63, 7 )
		pyxel.line( 168,  63, 173,  78, 7 )
		pyxel.line( 173,  78, 173, 145, 7 )
		pyxel.line( 173, 145, 173, 249, 7 )
		pyxel.line( 173, 249, 161, 249, 7 )
		pyxel.line( 161, 249, 161, 145, 7 )
		pyxel.line( 161, 145, 161,  90, 7 )
		pyxel.line( 161,  90, 159,  87, 7 )
		pyxel.line( 159,  87, 157,  90, 7 )
		pyxel.line( 157,  90, 157, 206, 7 )
		pyxel.line( 157, 206,  94, 255, 7 )

		#ホールデザイン
		for _set in range(len(hole_pic_tbl)//4):

			#斜めラインだけは始点から終点の線だけにする
			if( ( _set >= 4 ) and (_set <= 7 ) ):
				_num1 = hole_pic_tbl[_set * 4 + 0]
				_num2 = hole_pic_tbl[_set * 4 + 3]
				x1 = hole_pos_tbl[_num1 * 2 + 0]
				y1 = hole_pos_tbl[_num1 * 2 + 1]
				x2 = hole_pos_tbl[_num2 * 2 + 0]
				y2 = hole_pos_tbl[_num2 * 2 + 1]
				pyxel.line( x1,y1,x2,y2,1 )
			else:
				for _cnt in range(4):
					_num1 = hole_pic_tbl[_set * 4 + _cnt]
					_cnt2 = ( _cnt + 1 ) & 3
					_num2 = hole_pic_tbl[_set * 4 + _cnt2]
					
					x1 = hole_pos_tbl[_num1 * 2 + 0]
					y1 = hole_pos_tbl[_num1 * 2 + 1]
					x2 = hole_pos_tbl[_num2 * 2 + 0]
					y2 = hole_pos_tbl[_num2 * 2 + 1]
					pyxel.line( x1,y1,x2,y2,1 )

		#揃ったら色変えるとかしたい
		_is_perfect = 1
		for _set in range(len(hole_pic_tbl)//4):

			#斜めラインだけは始点から終点の線だけにする
			if( ( _set >= 4 ) and (_set <= 7 ) ):
				_num1 = hole_pic_tbl[_set * 4 + 0]
				_num2 = hole_pic_tbl[_set * 4 + 3]
				x1 = hole_pos_tbl[_num1 * 2 + 0]
				y1 = hole_pos_tbl[_num1 * 2 + 1]
				x2 = hole_pos_tbl[_num2 * 2 + 0]
				y2 = hole_pos_tbl[_num2 * 2 + 1]

				if( GWK[hole_pic_switch + _set] != 0 ):
					pyxel.line( x1,y1,x2,y2,10 )
				else:
					_is_perfect = 0
			else:
				for _cnt in range(4):
					_num1 = hole_pic_tbl[_set * 4 + _cnt]
					_cnt2 = ( _cnt + 1 ) & 3
					_num2 = hole_pic_tbl[_set * 4 + _cnt2]
					
					x1 = hole_pos_tbl[_num1 * 2 + 0]
					y1 = hole_pos_tbl[_num1 * 2 + 1]
					x2 = hole_pos_tbl[_num2 * 2 + 0]
					y2 = hole_pos_tbl[_num2 * 2 + 1]

					if( GWK[hole_pic_switch + _set] != 0 ):
						pyxel.line( x1,y1,x2,y2,10 )
					else:
						_is_perfect = 0

		if( _is_perfect ):
			if( ( GWK[game_adv] == G_GAME ) and ( GWK[game_subadv] == GS_MAIN ) ):
				GWK[game_subadv] = GS_PERFECT


		#シュートゲートの開閉
		if( GWK[shooter_gate_switch] & B_GATE_CLOSED ):
			pyxel.line(  159, 87,  173, 78, 10 )

		#ホール
		hole_size = len(hole_pos_tbl)//2
		for _cnt in range(hole_size):
			x, y = self.hole_body[_cnt].position
			pyxel.circ( x, y, 7, 7 )
			pyxel.circ( x, y, 6, 13 )	#白穴

		#軸
		shaft_size = len(shaft_pos_tbl)//2
		for _cnt in range(shaft_size):
			x, y = self.shaft_body[_cnt].position
			self.cput( x-1, y-3, 0x00 )

		#ストッパーバンパー
		x, y = self.bumper_body.position
		pyxel.circ(x-2, y-2, 4, 4)

		#シューター
		x, y = self.shooter_body.position
		pyxel.rect( x-5, y, 11, 5, 9 )
		pyxel.rect( x-1, y+5, 3, 249 - (y+5), 9 )
		
		#ホールインしたボール
		for _cnt in range(BALL_MAX):
			if( GWK[ball_switch + _cnt] & BALLSW_HOLEIN ):
				x = GWK[hollin_pos + ( _cnt * 3 + 0 )] - 5
				y = GWK[hollin_pos + ( _cnt * 3 + 1 )] - 5
				angle = GWK[hollin_pos + ( _cnt * 3 + 2 )] * 180 / 3.14		#radian => degree
				angle = angle % 360
				if( GWK[ball_type] == 0 ):
					_id = int( ( angle * 16 ) / 360 ) + 0x11		#赤
				else:
					_id = int( ( angle * 16 ) / 360 ) + 0x01		#青
				pyxel.blt( x, y, 0, self.ctbl[_id][0], self.ctbl[_id][1], self.ctbl[_id][2], self.ctbl[_id][3], 0 )


		#摩擦係数をセットすることでボールの回転が表現できる
		#ボール
		if( GWK[shooter_ball] != (-1) ):
			setnum = GWK[shooter_ball]
			x, y, *_ = self.ball_shape[setnum].bb
			angle = self.ball_shape[setnum].body.angle * 180 / 3.14		#radian => degree
			angle = angle % 360
			
			#ボールの見た目だけ移動
			if( GWK[ball_switch+setnum] & BALLSW_READY ):
				if( GWK[shooter_power] > 0 ):
					y = (180 + GWK[shooter_power] * PULL_PARAM / ADD_POWER_MAX)-11
			
			if( GWK[ball_type] == 0 ):
				_id = int( ( angle * 16 ) / 360 ) + 0x11		#赤
			else:
				_id = int( ( angle * 16 ) / 360 ) + 0x01		#青
			pyxel.blt( x, y, 0, self.ctbl[_id][0], self.ctbl[_id][1], self.ctbl[_id][2], self.ctbl[_id][3], 0 )


	#-----------------------------------------------------------------
	#入力（キーボード＆ジョイパッド）
	#-----------------------------------------------------------------
	#button-A（決定）
	def getInputA(self):
		if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
			return 1
		else:
			return 0

	#button-A（押下）
	def getPushA(self):
		if pyxel.btn( pyxel.KEY_Z ) or pyxel.btn( pyxel.GAMEPAD1_BUTTON_A ):
			return 1
		else:
			return 0

	#button-B（キャンセル）
	def getInputB(self):
		if pyxel.btnp(pyxel.KEY_X, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=10, repeat=10):
			return 1
		else:
			return 0

	#button-Y
	def getInputY(self):
		if pyxel.btnp(pyxel.KEY_Y, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y, hold=10, repeat=10):
			return 1
		else:
			return 0

if __name__ == "__main__":
	import pymunk

	FPS = 60
	App(pymunk, FPS)
