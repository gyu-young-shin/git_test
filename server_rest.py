
import tkinter
import tkinter.font
import threading 
import socket
import binascii
import datetime
import time
import logging
#---------------------------------------#
# for Logger                            #
#---------------------------------------#
# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#---------------------------------------#
# for Server                           #
#---------------------------------------#
count = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.89', 38000))    # ip주소, 포트번호 지정
server_socket.listen(socket.SOMAXCONN) 
print('echo server start')                         # 클라이언트의 연결요청을 기다리는 상태

ThreadTerminated =0
def SocketReadThreadFuncTheead():
    global ThreadTerminated

    while True:
        global client_socket
        client_socket, addr = server_socket.accept()
        if not client_socket:
            continue
        print ('connected host: {0} port: {1}'.format(addr[0], addr[1]))
        print("Socket Reading")
        logger.info('Start Echo Server')
        
        while 1:
            try:        
            # m_ReceiveEvent = win32event.CreateEvent(None, 0, 0, None)
            # m_objPCANBasic.SetValue(m_PcanHandle, PCAN_RECEIVE_EVENT, m_ReceiveEvent)
            # if(ThreadTerminated == 1):
            #     print("break thread")
            #     break
            
                data = client_socket.recv(2048)                 # 클라이언트로 부터 데이터를 받음. 출력되는 버퍼 사이즈. (만약 2할 경우, 2개의 데이터만 전송됨)
                # print("받은 데이터:", data.decode())
                print('recv msg:', binascii.hexlify(data))
            
                if(((data[0] == 0x23) & (data[3] == 0x01)) | ((data[0] == 0x23) & (data[3] == 0x11)) ):
                    length = data[1] <<8 | data[2]
                    print('length:', length)
                    if(length == 0x00):
                        print("data no" )
                        continue
                    if(data[3] == 0x01):
                        logger.info(f'{data[3]} State Chagne')
                    if(data[8]==0x00): # SID 
                        battery01 = (data[11] <<8 | data[12] )
                        print(data[8], data[9], data[10], float(battery01/10) )
                        btc['text'] = float(battery01/10) 
                        #-----------------------------    
                        if(data[9] & 0x01): # 도어(EM Lock, Dead Bolt) 
                            bt2['bg'] = 'red' 
                        else:
                            bt2['bg'] = 'white'
                                
                        if(data[9] & 0x02): # Em Lock 단선 여부 
                            bt3['bg'] = 'red' 
                        else:
                            bt3['bg'] = 'white'
                            
                        if(data[9] & 0x04): # AC(220V) 정전 여부
                            bt4['bg'] = 'red' 
                        else:
                            bt4['bg'] = 'white'   
                        if(data[9] & 0x08): # Battery 방전 여부  
                            bt5['bg'] = 'red' 
                        else:
                            bt5['bg'] = 'white' 
                        #-----------------------------     
                        if(data[9] & 0x10): # 개패장치 Cover 
                            bt6['bg'] = 'green' 
                        else:
                            bt6['bg'] = 'red'
                                
                        if(data[9] & 0x20): # 화재신호 입력 여부 
                            bt7['bg'] = 'red' 
                        else:
                            bt7['bg'] = 'white'
                            
                        if(data[9] & 0x40): # 비상버튼 입력 여부 
                            bt8['bg'] = 'red' 
                        else:
                            bt8['bg'] = 'white'   
                        if(data[9] & 0x80): # Slave RF 통신 상태  
                            bt9['bg'] = 'red' 
                        else:
                            bt9['bg'] = 'white'                         
                            
                        #-----------------------------    
                        if(data[10] & 0x01): # Password open 
                            bta['bg'] = 'red' 
                        else:
                            bta['bg'] = 'white'
                        if(data[10] & 0x02): # card open 
                            btb['bg'] = 'red' 
                        else:
                            btb['bg'] = 'white'
                        #----------------------------- 
                    if length >= 14:                          # SID | data1 | data2| battry |
                        if(data[13]==0x01):   # SID            # 13  |   14  |   15 | 16 17  |
                            battery02 = (data[16] <<8 | data[17] )
                            print(data[13] ,data[14], data[15], float(battery02/10) )
                            bstc['text'] = float(battery02/10) 
                            if(data[14] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bst2['bg'] = 'red' 
                            else:
                                bst2['bg'] = 'white'
                            if(data[14] & 0x02): # Em Lock 단선 여부 
                                bst3['bg'] = 'red' 
                            else:
                                bst3['bg'] = 'white'
                            
                            if(data[14] & 0x04): # AC(220V) 정전 여부
                                bst4['bg'] = 'red' 
                            else:
                                bst4['bg'] = 'white'   
                            if(data[14] & 0x08): # Battery 방전 여부  
                                bst5['bg'] = 'red' 
                            else:
                                bst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[14] & 0x10): # 개패장치 Cover 
                                bst6['bg'] = 'green' 
                            else:
                                bst6['bg'] = 'red'
                            if(data[14] & 0x20): # 화재신호 입력 여부 
                                bst7['bg'] = 'red' 
                            else:
                                bst7['bg'] = 'white'
                            if(data[14] & 0x40): # 비상버튼 입력 여부 
                                bst8['bg'] = 'red' 
                            else:
                                bst8['bg'] = 'white'   
                            if(data[14] & 0x80): # Slave RF 통신 상태  
                                bst9['bg'] = 'red' 
                                logger.info('중계기 RF 신호이상')
                            else:
                                bst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[15] & 0x01): # Password open 
                                bsta['bg'] = 'red' 
                            else:
                                bsta['bg'] = 'white'
                            if(data[15] & 0x02): # card open 
                                bstb['bg'] = 'red' 
                            else:
                                bstb['bg'] = 'white'
                            #----------------------------- 
                    if length >= 19:                          # SID | data1 | data2| battry |
                        if(data[18]==0x02):   # SID            # 18  |   19  |   20 | 21 22  |
                            battery03 = (data[21] <<8 | data[22] )
                            print(data[18], data[19], data[20], float(battery03/10) )
                            bsstc['text'] = float(battery03/10) 
                            if(data[19] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bsst2['bg'] = 'red' 
                            else:
                                bsst2['bg'] = 'white'
                                
                            if(data[19] & 0x02): # Em Lock 단선 여부 
                                bsst3['bg'] = 'red' 
                            else:
                                bsst3['bg'] = 'white'
                            
                            if(data[19] & 0x04): # AC(220V) 정전 여부
                                bsst4['bg'] = 'red' 
                            else:
                                bsst4['bg'] = 'white'   
                            if(data[19] & 0x08): # Battery 방전 여부  
                                bsst5['bg'] = 'red' 
                            else:
                                bsst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[19] & 0x10): # 개패장치 Cover 
                                bsst6['bg'] = 'green' 
                            else:
                                bsst6['bg'] = 'red'
                                
                            if(data[19] & 0x20): # 화재신호 입력 여부 
                                bsst7['bg'] = 'red' 
                            else:
                                bsst7['bg'] = 'white'
                            if(data[19] & 0x40): # 비상버튼 입력 여부 
                                bsst8['bg'] = 'red' 
                            else:
                                bsst8['bg'] = 'white'   
                            if(data[19] & 0x80): # Slave RF 통신 상태  
                                bsst9['bg'] = 'red' 
                            else:
                                bsst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[20] & 0x01): # Password open 
                                bssta['bg'] = 'red' 
                            else:
                                bssta['bg'] = 'white'
                            if(data[20] & 0x02): # card open 
                                bsstb['bg'] = 'red' 
                            else:
                                bsstb['bg'] = 'white'
                                
                    if length >= 24:                          # SID | data1 | data2| battry | slave-3
                        if(data[23]==0x03):   # SID            # 23  |   24  |   25 | 26 27  |
                            battery04 = (data[26] <<8 | data[27] )
                            print(data[23], data[24], data[25], float(battery04/10) )
                            bssstc['text'] = float(battery04/10) 
                            if(data[24] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bssst2['bg'] = 'red' 
                            else:
                                bssst2['bg'] = 'white'
                                
                            if(data[24] & 0x02): # Em Lock 단선 여부 
                                bssst3['bg'] = 'red' 
                            else:
                                bssst3['bg'] = 'white'
                            
                            if(data[24] & 0x04): # AC(220V) 정전 여부
                                bssst4['bg'] = 'red' 
                            else:
                                bssst4['bg'] = 'white'   
                            if(data[24] & 0x08): # Battery 방전 여부  
                                bssst5['bg'] = 'red' 
                            else:
                                bssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[24] & 0x10): # 개패장치 Cover 
                                bssst6['bg'] = 'green' 
                            else:
                                bssst6['bg'] = 'red'
                                
                            if(data[24] & 0x20): # 화재신호 입력 여부 
                                bssst7['bg'] = 'red' 
                            else:
                                bssst7['bg'] = 'white'
                            if(data[24] & 0x40): # 비상버튼 입력 여부 
                                bssst8['bg'] = 'red' 
                            else:
                                bssst8['bg'] = 'white'   
                            if(data[24] & 0x80): # Slave RF 통신 상태  
                                bssst9['bg'] = 'red' 
                            else:
                                bssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[25] & 0x01): # Password open 
                                bsssta['bg'] = 'red' 
                            else:
                                bsssta['bg'] = 'white'
                            if(data[25] & 0x02): # card open 
                                bssstb['bg'] = 'red' 
                            else:
                                bssstb['bg'] = 'white'
                    if length >= 29:                          # SID | data1 | data2| battry | slave-4
                        if(data[28]==0x04):   # SID            # 28  |   29  |   30 | 31 32  |
                            battery05 = (data[31] <<8 | data[32] )
                            print(data[28], data[29], data[30], float(battery05/10) )
                            bsssstc['text'] = float(battery05/10) 
                            if(data[29] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bsssst2['bg'] = 'red' 
                            else:
                                bsssst2['bg'] = 'white'
                                
                            if(data[29] & 0x02): # Em Lock 단선 여부 
                                bsssst3['bg'] = 'red' 
                            else:
                                bsssst3['bg'] = 'white'
                            
                            if(data[29] & 0x04): # AC(220V) 정전 여부
                                bsssst4['bg'] = 'red' 
                            else:
                                bsssst4['bg'] = 'white'   
                            if(data[29] & 0x08): # Battery 방전 여부  
                                bsssst5['bg'] = 'red' 
                            else:
                                bsssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[29] & 0x10): # 개패장치 Cover 
                                bsssst6['bg'] = 'green' 
                            else:
                                bsssst6['bg'] = 'red'
                                
                            if(data[29] & 0x20): # 화재신호 입력 여부 
                                bsssst7['bg'] = 'red' 
                            else:
                                bsssst7['bg'] = 'white'
                            if(data[29] & 0x40): # 비상버튼 입력 여부 
                                bsssst8['bg'] = 'red' 
                            else:
                                bsssst8['bg'] = 'white'   
                            if(data[29] & 0x80): # Slave RF 통신 상태  
                                bsssst9['bg'] = 'red' 
                            else:
                                bsssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[30] & 0x01): # Password open 
                                bssssta['bg'] = 'red' 
                            else:
                                bssssta['bg'] = 'white'
                            if(data[30] & 0x02): # card open 
                                bsssstb['bg'] = 'red' 
                            else:
                                bsssstb['bg'] = 'white'
                    if length >= 34:                         # SID | data1 | data2| battry |  slave-5
                        if(data[33]==0x05):   # SID          # 33  |   34  |  35  | 36 37  |
                            battery06 = (data[36] <<8 | data[37] )
                            print(data[33], data[34], data[35], float(battery06/10) )
                            bssssstc['text'] = float(battery06/10) 
                            if(data[34] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bssssst2['bg'] = 'red' 
                            else:
                                bssssst2['bg'] = 'white'
                                
                            if(data[34] & 0x02): # Em Lock 단선 여부 
                                bssssst3['bg'] = 'red' 
                            else:
                                bssssst3['bg'] = 'white'
                            
                            if(data[34] & 0x04): # AC(220V) 정전 여부
                                bssssst4['bg'] = 'red' 
                            else:
                                bssssst4['bg'] = 'white'   
                            if(data[34] & 0x08): # Battery 방전 여부  
                                bssssst5['bg'] = 'red' 
                            else:
                                bssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[34] & 0x10): # 개패장치 Cover 
                                bssssst6['bg'] = 'green' 
                            else:
                                bssssst6['bg'] = 'red'
                                
                            if(data[34] & 0x20): # 화재신호 입력 여부 
                                bssssst7['bg'] = 'red' 
                            else:
                                bssssst7['bg'] = 'white'
                            if(data[34] & 0x40): # 비상버튼 입력 여부 
                                bssssst8['bg'] = 'red' 
                            else:
                                bssssst8['bg'] = 'white'   
                            if(data[34] & 0x80): # Slave RF 통신 상태  
                                bssssst9['bg'] = 'red' 
                            else:
                                bssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[35] & 0x01): # Password open 
                                bsssssta['bg'] = 'red' 
                            else:
                                bsssssta['bg'] = 'white'
                            if(data[35] & 0x02): # card open 
                                bssssstb['bg'] = 'red' 
                            else:
                                bssssstb['bg'] = 'white'
                    if length >= 39:                         # SID | data1 | data2| battry |  slave-6
                        if(data[38]==0x06):   # SID          # 38  |   39  |  40  | 41 42  |
                            battery07 = (data[41] <<8 | data[42] )
                            print(data[38], data[39], data[40], float(battery07/10) )
                            bsssssstc['text'] = float(battery07/10) 
                            if(data[39] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bsssssst2['bg'] = 'red' 
                            else:
                                bsssssst2['bg'] = 'white'
                                
                            if(data[39] & 0x02): # Em Lock 단선 여부 
                                bsssssst3['bg'] = 'red' 
                            else:
                                bsssssst3['bg'] = 'white'
                            
                            if(data[39] & 0x04): # AC(220V) 정전 여부
                                bsssssst4['bg'] = 'red' 
                            else:
                                bsssssst4['bg'] = 'white'   
                            if(data[39] & 0x08): # Battery 방전 여부  
                                bsssssst5['bg'] = 'red' 
                            else:
                                bsssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[39] & 0x10): # 개패장치 Cover 
                                bsssssst6['bg'] = 'green' 
                            else:
                                bsssssst6['bg'] = 'red'
                                
                            if(data[39] & 0x20): # 화재신호 입력 여부 
                                bsssssst7['bg'] = 'red' 
                            else:
                                bsssssst7['bg'] = 'white'
                            if(data[39] & 0x40): # 비상버튼 입력 여부 
                                bsssssst8['bg'] = 'red' 
                            else:
                                bsssssst8['bg'] = 'white'   
                            if(data[39] & 0x80): # Slave RF 통신 상태  
                                bsssssst9['bg'] = 'red' 
                            else:
                                bsssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[40] & 0x01): # Password open 
                                bssssssta['bg'] = 'red' 
                            else:
                                bssssssta['bg'] = 'white'
                            if(data[40] & 0x02): # card open 
                                bsssssstb['bg'] = 'red' 
                            else:
                                bsssssstb['bg'] = 'white'     
                                
                    if length >= 44:                         # SID | data1 | data2| battry |  slave-7
                        if(data[43]==0x07):   # SID          # 43  |   44  |  45  | 46 47  |
                            battery08 = (data[46] <<8 | data[47] )
                            print(data[43], data[44], data[45], float(battery08/10) )
                            bssssssstc['text'] = float(battery08/10) 
                            if(data[44] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bssssssst2['bg'] = 'red' 
                            else:
                                bssssssst2['bg'] = 'white'
                                
                            if(data[44] & 0x02): # Em Lock 단선 여부 
                                bssssssst3['bg'] = 'red' 
                            else:
                                bssssssst3['bg'] = 'white'
                            
                            if(data[44] & 0x04): # AC(220V) 정전 여부
                                bssssssst4['bg'] = 'red' 
                            else:
                                bssssssst4['bg'] = 'white'   
                            if(data[44] & 0x08): # Battery 방전 여부  
                                bssssssst5['bg'] = 'red' 
                            else:
                                bssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[44] & 0x10): # 개패장치 Cover 
                                bssssssst6['bg'] = 'green' 
                            else:
                                bssssssst6['bg'] = 'red'
                                
                            if(data[44] & 0x20): # 화재신호 입력 여부 
                                bssssssst7['bg'] = 'red' 
                            else:
                                bssssssst7['bg'] = 'white'
                            if(data[44] & 0x40): # 비상버튼 입력 여부 
                                bssssssst8['bg'] = 'red' 
                            else:
                                bssssssst8['bg'] = 'white'   
                            if(data[44] & 0x80): # Slave RF 통신 상태  
                                bssssssst9['bg'] = 'red' 
                            else:
                                bssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[45] & 0x01): # Password open 
                                bsssssssta['bg'] = 'red' 
                            else:
                                bsssssssta['bg'] = 'white'
                            if(data[45] & 0x02): # card open 
                                bssssssstb['bg'] = 'red' 
                            else:
                                bssssssstb['bg'] = 'white'         
    
                    if length >= 49:                         # SID | data1 | data2| battry |  slave-8
                        if(data[48]==0x08):   # SID          # 48  |   49  |  50  | 51 52  |
                            battery09 = (data[51] <<8 | data[52] )
                            print(data[48], data[49], data[50], float(battery09/10) )
                            bsssssssstc['text'] = float(battery09/10) 
                            if(data[49] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bsssssssst2['bg'] = 'red' 
                            else:
                                bsssssssst2['bg'] = 'white'
                                
                            if(data[49] & 0x02): # Em Lock 단선 여부 
                                bsssssssst3['bg'] = 'red' 
                            else:
                                bsssssssst3['bg'] = 'white'
                            
                            if(data[49] & 0x04): # AC(220V) 정전 여부
                                bsssssssst4['bg'] = 'red' 
                            else:
                                bsssssssst4['bg'] = 'white'   
                            if(data[49] & 0x08): # Battery 방전 여부  
                                bsssssssst5['bg'] = 'red' 
                            else:
                                bsssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[49] & 0x10): # 개패장치 Cover 
                                bsssssssst6['bg'] = 'green' 
                            else:
                                bsssssssst6['bg'] = 'red'
                                
                            if(data[49] & 0x20): # 화재신호 입력 여부 
                                bsssssssst7['bg'] = 'red' 
                            else:
                                bsssssssst7['bg'] = 'white'
                            if(data[49] & 0x40): # 비상버튼 입력 여부 
                                bsssssssst8['bg'] = 'red' 
                            else:
                                bsssssssst8['bg'] = 'white'   
                            if(data[49] & 0x80): # Slave RF 통신 상태  
                                bsssssssst9['bg'] = 'red' 
                            else:
                                bsssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[50] & 0x01): # Password open 
                                bssssssssta['bg'] = 'red' 
                            else:
                                bssssssssta['bg'] = 'white'
                            if(data[50] & 0x02): # card open 
                                bsssssssstb['bg'] = 'red' 
                            else:
                                bsssssssstb['bg'] = 'white'     
                                
                    if length >= 54:                         # SID | data1 | data2| battry |  slave-9
                        if(data[53]==0x09):   # SID          # 53  |   54  |  55  | 56 57  |
                            battery10 = (data[56] <<8 | data[57] )
                            print(data[53], data[54], data[55], float(battery10/10) )
                            bssssssssstc['text'] = float(battery10/10) 
                            if(data[54] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bssssssssst2['bg'] = 'red' 
                            else:
                                bssssssssst2['bg'] = 'white'
                                
                            if(data[54] & 0x02): # Em Lock 단선 여부 
                                bssssssssst3['bg'] = 'red' 
                            else:
                                bssssssssst3['bg'] = 'white'
                            
                            if(data[54] & 0x04): # AC(220V) 정전 여부
                                bssssssssst4['bg'] = 'red' 
                            else:
                                bssssssssst4['bg'] = 'white'   
                            if(data[54] & 0x08): # Battery 방전 여부  
                                bssssssssst5['bg'] = 'red' 
                            else:
                                bssssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[54] & 0x10): # 개패장치 Cover 
                                bssssssssst6['bg'] = 'green' 
                            else:
                                bssssssssst6['bg'] = 'red'
                                
                            if(data[54] & 0x20): # 화재신호 입력 여부 
                                bssssssssst7['bg'] = 'red' 
                            else:
                                bssssssssst7['bg'] = 'white'
                            if(data[54] & 0x40): # 비상버튼 입력 여부 
                                bssssssssst8['bg'] = 'red' 
                            else:
                                bssssssssst8['bg'] = 'white'   
                            if(data[54] & 0x80): # Slave RF 통신 상태  
                                bssssssssst9['bg'] = 'red' 
                            else:
                                bssssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[55] & 0x01): # Password open 
                                bsssssssssta['bg'] = 'red' 
                            else:
                                bsssssssssta['bg'] = 'white'
                            if(data[55] & 0x02): # card open 
                                bssssssssstb['bg'] = 'red' 
                            else:
                                bssssssssstb['bg'] = 'white'     
                    if length >= 59:                         # SID | data1 | data2| battry |  slave-10
                        if(data[58]==0x0a):   # SID          # 58  |   59  |  60  | 61 62  |
                            battery11 = (data[61] <<8 | data[62] )
                            print(data[58], data[59], data[60], float(battery11/10) )
                            bsssssssssstc['text'] = float(battery11/10) 
                            if(data[59] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                bsssssssssst2['bg'] = 'red' 
                            else:
                                bsssssssssst2['bg'] = 'white'
                                
                            if(data[59] & 0x02): # Em Lock 단선 여부 
                                bsssssssssst3['bg'] = 'red' 
                            else:
                                bsssssssssst3['bg'] = 'white'
                            
                            if(data[59] & 0x04): # AC(220V) 정전 여부
                                bsssssssssst4['bg'] = 'red' 
                            else:
                                bsssssssssst4['bg'] = 'white'   
                            if(data[59] & 0x08): # Battery 방전 여부  
                                bsssssssssst5['bg'] = 'red' 
                            else:
                                bsssssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[59] & 0x10): # 개패장치 Cover 
                                bsssssssssst6['bg'] = 'green' 
                            else:
                                bsssssssssst6['bg'] = 'red'
                                
                            if(data[59] & 0x20): # 화재신호 입력 여부 
                                bsssssssssst7['bg'] = 'red' 
                            else:
                                bsssssssssst7['bg'] = 'white'
                            if(data[59] & 0x40): # 비상버튼 입력 여부 
                                bsssssssssst8['bg'] = 'red' 
                            else:
                                bsssssssssst8['bg'] = 'white'   
                            if(data[59] & 0x80): # Slave RF 통신 상태  
                                bsssssssssst9['bg'] = 'red' 
                            else:
                                bsssssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[60] & 0x01): # Password open 
                                bssssssssssta['bg'] = 'red' 
                            else:
                                bssssssssssta['bg'] = 'white'
                            if(data[60] & 0x02): # card open 
                                bsssssssssstb['bg'] = 'red' 
                            else:
                                bsssssssssstb['bg'] = 'white'  
                                
                    if length >= 64:                         # SID | data1 | data2| battry |  slave-11
                        if(data[63]==0x0b):   # SID          # 63  |   64  |  65  | 66 67  |
                            battery12 = (data[66] <<8 | data[67] )
                            print(data[63], data[64], data[65], float(battery12/10) )
                            basssssssssstc['text'] = float(battery12/10) 
                            if(data[64] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                basssssssssst2['bg'] = 'red' 
                            else:
                                basssssssssst2['bg'] = 'white'
                                
                            if(data[64] & 0x02): # Em Lock 단선 여부 
                                basssssssssst3['bg'] = 'red' 
                            else:
                                basssssssssst3['bg'] = 'white'
                            
                            if(data[64] & 0x04): # AC(220V) 정전 여부
                                basssssssssst4['bg'] = 'red' 
                            else:
                                basssssssssst4['bg'] = 'white'   
                            if(data[64] & 0x08): # Battery 방전 여부  
                                basssssssssst5['bg'] = 'red' 
                            else:
                                basssssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[64] & 0x10): # 개패장치 Cover 
                                basssssssssst6['bg'] = 'green' 
                            else:
                                basssssssssst6['bg'] = 'red'
                                
                            if(data[64] & 0x20): # 화재신호 입력 여부 
                                basssssssssst7['bg'] = 'red' 
                            else:
                                basssssssssst7['bg'] = 'white'
                            if(data[64] & 0x40): # 비상버튼 입력 여부 
                                basssssssssst8['bg'] = 'red' 
                            else:
                                basssssssssst8['bg'] = 'white'   
                            if(data[64] & 0x80): # Slave RF 통신 상태  
                                basssssssssst9['bg'] = 'red' 
                            else:
                                basssssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[65] & 0x01): # Password open 
                                bassssssssssta['bg'] = 'red' 
                            else:
                                bassssssssssta['bg'] = 'white'
                            if(data[65] & 0x02): # card open 
                                basssssssssstb['bg'] = 'red' 
                            else:
                                basssssssssstb['bg'] = 'white'  
                                
                    if length >= 69:                         # SID | data1 | data2| battry |  slave-12
                        if(data[68]==0x0c):   # SID          # 68  |   69  |  70  | 71 72  |
                            battery13 = (data[71] <<8 | data[72] )
                            print(data[68], data[69], data[70], float(battery13/10) )
                            baasssssssssstc['text'] = float(battery13/10) 
                            if(data[69] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                baasssssssssst2['bg'] = 'red' 
                            else:
                                baasssssssssst2['bg'] = 'white'
                                
                            if(data[69] & 0x02): # Em Lock 단선 여부 
                                baasssssssssst3['bg'] = 'red' 
                            else:
                                baasssssssssst3['bg'] = 'white'
                            
                            if(data[69] & 0x04): # AC(220V) 정전 여부
                                baasssssssssst4['bg'] = 'red' 
                            else:
                                baasssssssssst4['bg'] = 'white'   
                            if(data[69] & 0x08): # Battery 방전 여부  
                                baasssssssssst5['bg'] = 'red' 
                            else:
                                baasssssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[69] & 0x10): # 개패장치 Cover 
                                baasssssssssst6['bg'] = 'green' 
                            else:
                                baasssssssssst6['bg'] = 'red'
                                
                            if(data[69] & 0x20): # 화재신호 입력 여부 
                                baasssssssssst7['bg'] = 'red' 
                            else:
                                baasssssssssst7['bg'] = 'white'
                            if(data[69] & 0x40): # 비상버튼 입력 여부 
                                baasssssssssst8['bg'] = 'red' 
                            else:
                                baasssssssssst8['bg'] = 'white'   
                            if(data[69] & 0x80): # Slave RF 통신 상태  
                                baasssssssssst9['bg'] = 'red' 
                            else:
                                baasssssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[70] & 0x01): # Password open 
                                baassssssssssta['bg'] = 'red' 
                                logger.info(f'{data[68]} Slave Password Open.')
                            else:
                                baassssssssssta['bg'] = 'white'
                            if(data[70] & 0x02): # card open 
                                baasssssssssstb['bg'] = 'red' 
                                logger.info(f'{data[68]} Slave Card Open.')
                            else:
                                baasssssssssstb['bg'] = 'white' 
                                
                    if length >= 74:                         # SID | data1 | data2| battry |  slave-13
                        if(data[73]==0x0d):   # SID          # 73  |   74  |  75  | 76 77  |
                            battery13 = (data[76] <<8 | data[77] )
                            print(data[73], data[74], data[75], float(battery13/10) )
                            baaasssssssssstc['text'] = float(battery13/10) 
                            if(data[74] & 0x01): # 도어(EM Lock, Dead Bolt) 
                                baaasssssssssst2['bg'] = 'red' 
                            else:
                                baaasssssssssst2['bg'] = 'white'
                                
                            if(data[74] & 0x02): # Em Lock 단선 여부 
                                baaasssssssssst3['bg'] = 'red' 
                            else:
                                baaasssssssssst3['bg'] = 'white'
                            
                            if(data[74] & 0x04): # AC(220V) 정전 여부
                                baaasssssssssst4['bg'] = 'red' 
                            else:
                                baaasssssssssst4['bg'] = 'white'   
                            if(data[74] & 0x08): # Battery 방전 여부  
                                baaasssssssssst5['bg'] = 'red' 
                            else:
                                baaasssssssssst5['bg'] = 'white' 
                            #-----------------------------     
                            if(data[74] & 0x10): # 개패장치 Cover 
                                baaasssssssssst6['bg'] = 'green' 
                            else:
                                baaasssssssssst6['bg'] = 'red'
                                
                            if(data[74] & 0x20): # 화재신호 입력 여부 
                                baaasssssssssst7['bg'] = 'red' 
                            else:
                                baaasssssssssst7['bg'] = 'white'
                            if(data[74] & 0x40): # 비상버튼 입력 여부 
                                baaasssssssssst8['bg'] = 'red' 
                            else:
                                baaasssssssssst8['bg'] = 'white'   
                            if(data[74] & 0x80): # Slave RF 통신 상태  
                                baaasssssssssst9['bg'] = 'red' 
                            else:
                                baaasssssssssst9['bg'] = 'white'                         
                            #-----------------------------    
                            if(data[75] & 0x01): # Password open 
                                baaassssssssssta['bg'] = 'red' 
                                # logger.info(f'{data[73]} Slave Password Open.')
                            else:
                                baaassssssssssta['bg'] = 'white'
                            if(data[75] & 0x02): # card open 
                                baaasssssssssstb['bg'] = 'red' 
                                # logger.info(f'{data[73]} Slave Card Open.')
                            else:
                                baaasssssssssstb['bg'] = 'white'                              
                else:
                    continue
                    #----------------------------- 
                print("--------------------------------")
            
            except:
                print('disconnected')
                break
            
def requestState():
    send_data = bytearray(b'\x23\x00\x01\xb1\x99')
    client_socket.send(send_data)


def requestUpdateTime():
    send_data = bytearray(b'\x23\x00\x01\xc1\x3c')
    client_socket.send(send_data)
    
    
t = threading.Thread(target=SocketReadThreadFuncTheead)
def SocketReadThreadFunc():
    timer_t()
    ConCliBT['bg'] = 'white'
    t.start()
    
    
def SocketClosed():
    global ThreadTerminated
    
    print('echo server terminater')   
    ThreadTerminated =1
    server_socket.close()
    t.join()
    
def timer_t():
    global count 
    global mode_test 
    count += 1
    # print(count)
    timer = threading.Timer(1, timer_t)
    timer.start()
    if(count % 50 == 0 ):
        requestState()
        
window=tkinter.Tk()
window.title("비상문 관리 시스템 ")
window.geometry("650x400")
window.resizable(False, False)
ConCliBT = tkinter.Button(window, command = SocketReadThreadFunc, text="CONNECT" ,bg="green")
StopCliBT = tkinter.Button(window, command = requestUpdateTime, text="DISCONNECT" ,bg="green")
b1=tkinter.Label(window,width = "10", text=" SID "  , bg= "gray",relief="groove")
b2=tkinter.Label(window,width = "5 ", text="도 어 " , bg="yellow",relief="groove")
b3=tkinter.Label(window,width = "5 ", text="단 선 "  , bg="yellow",relief="groove")
b4=tkinter.Label(window,width = "5 ", text="정 전"  , bg="yellow",relief="groove")
b5=tkinter.Label(window,width = "5 ", text="방 전"  , bg="yellow",relief="groove")
b6=tkinter.Label(window,width = "5 ", text="커 버"  , bg="yellow",relief="groove")
b7=tkinter.Label(window,width = "5 ", text="화 재"  , bg="yellow",relief="groove")
b8=tkinter.Label(window,width = "5 ", text="비 상"  , bg="yellow",relief="groove")
b9=tkinter.Label(window,width = "5 ", text="R F "   , bg= "yellow",relief="groove")
ba=tkinter.Label(window,width = "5 ", text="P-Op"   , bg= "yellow",relief="groove")
bb=tkinter.Label(window,width = "5 ", text="C-Op"   , bg= "yellow",relief="groove")
bc=tkinter.Label(window,width = "8 ", text="BAT(V)" , bg= "yellow",relief="groove")
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)
b4.grid(row=0, column=3)
b5.grid(row=0, column=4)
b6.grid(row=0, column=5)
b7.grid(row=0, column=6)
b8.grid(row=0, column=7)
b9.grid(row=0, column=8)
ba.grid(row=0, column=9)
bb.grid(row=0, column=10)
bc.grid(row=0, column=11)
bt1=tkinter.Label(window,width = "10", text=" MASTER " ,bg="gray" ,relief="groove")
bt2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bt9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
btb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
btc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bt1.grid(row=1, column=0)
bt2.grid(row=1, column=1)
bt3.grid(row=1, column=2)
bt4.grid(row=1, column=3)
bt5.grid(row=1, column=4)
bt6.grid(row=1, column=5)
bt7.grid(row=1, column=6)
bt8.grid(row=1, column=7)
bt9.grid(row=1, column=8)
bta.grid(row=1, column=9)
btb.grid(row=1, column=10)
btc.grid(row=1, column=11)
bst1=tkinter.Label(window,width = "10", text=" SLAVE-1 ",bg="gray" ,relief="groove")
bst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bst1.grid(row=2, column=0)
bst2.grid(row=2, column=1)
bst3.grid(row=2, column=2)
bst4.grid(row=2, column=3)
bst5.grid(row=2, column=4)
bst6.grid(row=2, column=5)
bst7.grid(row=2, column=6)
bst8.grid(row=2, column=7)
bst9.grid(row=2, column=8)
bsta.grid(row=2, column=9)
bstb.grid(row=2, column=10)
bstc.grid(row=2, column=11)
bsst1=tkinter.Label(window,width = "10", text=" SLAVE-2 ",bg="gray" ,relief="groove")
bsst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bsst1.grid(row=3, column=0)
bsst2.grid(row=3, column=1)
bsst3.grid(row=3, column=2)
bsst4.grid(row=3, column=3)
bsst5.grid(row=3, column=4)
bsst6.grid(row=3, column=5)
bsst7.grid(row=3, column=6)
bsst8.grid(row=3, column=7)
bsst9.grid(row=3, column=8)
bssta.grid(row=3, column=9)
bsstb.grid(row=3, column=10)
bsstc.grid(row=3, column=11)
bssst1=tkinter.Label(window,width = "10", text=" SLAVE-3 ",bg="gray" ,relief="groove")
bssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bssst1.grid(row=4, column=0)
bssst2.grid(row=4, column=1)
bssst3.grid(row=4, column=2)
bssst4.grid(row=4, column=3)
bssst5.grid(row=4, column=4)
bssst6.grid(row=4, column=5)
bssst7.grid(row=4, column=6)
bssst8.grid(row=4, column=7)
bssst9.grid(row=4, column=8)
bsssta.grid(row=4, column=9)
bssstb.grid(row=4, column=10)
bssstc.grid(row=4, column=11)
bsssst1=tkinter.Label(window,width = "10", text=" SLAVE-4 ",bg="gray" ,relief="groove")
bsssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bsssst1.grid(row=5, column=0)
bsssst2.grid(row=5, column=1)
bsssst3.grid(row=5, column=2)
bsssst4.grid(row=5, column=3)
bsssst5.grid(row=5, column=4)
bsssst6.grid(row=5, column=5)
bsssst7.grid(row=5, column=6)
bsssst8.grid(row=5, column=7)
bsssst9.grid(row=5, column=8)
bssssta.grid(row=5, column=9)
bsssstb.grid(row=5, column=10)
bsssstc.grid(row=5, column=11)

bssssst1=tkinter.Label(window,width = "10", text=" SLAVE-5 ",bg="gray" ,relief="groove")
bssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bssssst1.grid(row=6, column=0)
bssssst2.grid(row=6, column=1)
bssssst3.grid(row=6, column=2)
bssssst4.grid(row=6, column=3)
bssssst5.grid(row=6, column=4)
bssssst6.grid(row=6, column=5)
bssssst7.grid(row=6, column=6)
bssssst8.grid(row=6, column=7)
bssssst9.grid(row=6, column=8)
bsssssta.grid(row=6, column=9)
bssssstb.grid(row=6, column=10)
bssssstc.grid(row=6, column=11)
bsssssst1=tkinter.Label(window,width = "10", text=" SLAVE-6 ",bg="gray" ,relief="groove")
bsssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bsssssst1.grid(row=7, column=0)
bsssssst2.grid(row=7, column=1)
bsssssst3.grid(row=7, column=2)
bsssssst4.grid(row=7, column=3)
bsssssst5.grid(row=7, column=4)
bsssssst6.grid(row=7, column=5)
bsssssst7.grid(row=7, column=6)
bsssssst8.grid(row=7, column=7)
bsssssst9.grid(row=7, column=8)
bssssssta.grid(row=7, column=9)
bsssssstb.grid(row=7, column=10)
bsssssstc.grid(row=7, column=11)
bssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-7 ",bg="gray" ,relief="groove")
bssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bssssssst1.grid(row=8, column=0)
bssssssst2.grid(row=8, column=1)
bssssssst3.grid(row=8, column=2)
bssssssst4.grid(row=8, column=3)
bssssssst5.grid(row=8, column=4)
bssssssst6.grid(row=8, column=5)
bssssssst7.grid(row=8, column=6)
bssssssst8.grid(row=8, column=7)
bssssssst9.grid(row=8, column=8)
bsssssssta.grid(row=8, column=9)
bssssssstb.grid(row=8, column=10)
bssssssstc.grid(row=8, column=11)
bsssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-8 ",bg="gray" ,relief="groove")
bsssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bsssssssst1.grid(row=9, column=0)
bsssssssst2.grid(row=9, column=1)
bsssssssst3.grid(row=9, column=2)
bsssssssst4.grid(row=9, column=3)
bsssssssst5.grid(row=9, column=4)
bsssssssst6.grid(row=9, column=5)
bsssssssst7.grid(row=9, column=6)
bsssssssst8.grid(row=9, column=7)
bsssssssst9.grid(row=9, column=8)
bssssssssta.grid(row=9, column=9)
bsssssssstb.grid(row=9, column=10)
bsssssssstc.grid(row=9, column=11)
bssssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-9 ",bg="gray" ,relief="groove")
bssssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bssssssssst1.grid(row=10, column=0)
bssssssssst2.grid(row=10, column=1)
bssssssssst3.grid(row=10, column=2)
bssssssssst4.grid(row=10, column=3)
bssssssssst5.grid(row=10, column=4)
bssssssssst6.grid(row=10, column=5)
bssssssssst7.grid(row=10, column=6)
bssssssssst8.grid(row=10, column=7)
bssssssssst9.grid(row=10, column=8)
bsssssssssta.grid(row=10, column=9)
bssssssssstb.grid(row=10, column=10)
bssssssssstc.grid(row=10, column=11)
bsssssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-10 ",bg="gray" ,relief="groove")
bsssssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bssssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bsssssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
bsssssssssst1.grid(row=11, column=0)
bsssssssssst2.grid(row=11, column=1)
bsssssssssst3.grid(row=11, column=2)
bsssssssssst4.grid(row=11, column=3)
bsssssssssst5.grid(row=11, column=4)
bsssssssssst6.grid(row=11, column=5)
bsssssssssst7.grid(row=11, column=6)
bsssssssssst8.grid(row=11, column=7)
bsssssssssst9.grid(row=11, column=8)
bssssssssssta.grid(row=11, column=9)
bsssssssssstb.grid(row=11, column=10)
bsssssssssstc.grid(row=11, column=11)
basssssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-11 ",bg="gray" ,relief="groove")
basssssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
bassssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
basssssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
basssssssssst1.grid(row=12, column=0)
basssssssssst2.grid(row=12, column=1)
basssssssssst3.grid(row=12, column=2)
basssssssssst4.grid(row=12, column=3)
basssssssssst5.grid(row=12, column=4)
basssssssssst6.grid(row=12, column=5)
basssssssssst7.grid(row=12, column=6)
basssssssssst8.grid(row=12, column=7)
basssssssssst9.grid(row=12, column=8)
bassssssssssta.grid(row=12, column=9)
basssssssssstb.grid(row=12, column=10)
basssssssssstc.grid(row=12, column=11)
baasssssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-12 ",bg="gray" ,relief="groove")
baasssssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baassssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baasssssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
baasssssssssst1.grid(row=13, column=0)
baasssssssssst2.grid(row=13, column=1)
baasssssssssst3.grid(row=13, column=2)
baasssssssssst4.grid(row=13, column=3)
baasssssssssst5.grid(row=13, column=4)
baasssssssssst6.grid(row=13, column=5)
baasssssssssst7.grid(row=13, column=6)
baasssssssssst8.grid(row=13, column=7)
baasssssssssst9.grid(row=13, column=8)
baassssssssssta.grid(row=13, column=9)
baasssssssssstb.grid(row=13, column=10)
baasssssssssstc.grid(row=13, column=11)

baaasssssssssst1=tkinter.Label(window,width = "10", text=" SLAVE-13 ",bg="gray" ,relief="groove")
baaasssssssssst2=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst3=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst4=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst5=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst6=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst7=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst8=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst9=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaassssssssssta=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssstb=tkinter.Label(window,width = "5 ", text=" "        ,bg="white",relief="groove")
baaasssssssssstc=tkinter.Label(window,width = "8 ", text=" "        ,bg="white",relief="groove")
baaasssssssssst1.grid(row=14, column=0)
baaasssssssssst2.grid(row=14, column=1)
baaasssssssssst3.grid(row=14, column=2)
baaasssssssssst4.grid(row=14, column=3)
baaasssssssssst5.grid(row=14, column=4)
baaasssssssssst6.grid(row=14, column=5)
baaasssssssssst7.grid(row=14, column=6)
baaasssssssssst8.grid(row=14, column=7)
baaasssssssssst9.grid(row=14, column=8)
baaassssssssssta.grid(row=14, column=9)
baaasssssssssstb.grid(row=14, column=10)
baaasssssssssstc.grid(row=14, column=11)
ConCliBT.place(x=550,y=10)
StopCliBT.place(x=550, y= 40)


window.mainloop()
