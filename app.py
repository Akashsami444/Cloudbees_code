import grpc
from concurrent import futures
import time
import ticket_reservation_pb2_grpc as pb2_grpc
import ticket_reservation_pb2 as pb2


class TicketReservationService(pb2_grpc.TicketReservationServicer):

    def __init__(self, *args, **kwargs):
        self.seat_db = {"A":[None]*20,"B":[None]*20}
        self.ticket_db = {}
        self.ticket_counter = 0

    def ReserveTicket(self, request, context):
        self.ticket_counter+=1
        # get the string from the incoming request
        print(request)
        from_code = request.from_code
        response = {'from_code':request.from_code,'to_code':request.to_code, 'price_paid':request.price_paid, 'passenger_count':request.passenger_count,'passengers':[]}
        for i in range(response['passenger_count']):
            response['passengers'].append({})
            response['passengers'][i]['first_name'] = request.passengers[i].first_name
            response['passengers'][i]['last_name'] = request.passengers[i].last_name
            response['passengers'][i]['email'] = request.passengers[i].email
            response['passengers'][i]['address'] = request.passengers[i].address
            isReserved = False
            if not(request.passengers[i].section is None or request.passengers[i].section == '') and self.seat_db[request.passengers[i].section][request.passengers[i].seat-1] is not None:
                if None in self.seat_db[request.passengers[i].section]:
                    for j in range(len(self.seat_db[request.passengers[i].section])):
                        if self.seat_db[request.passengers[i].section][j] is None:
                            response['passengers'][i]['seat'] = j+1
                            response['passengers'][i]['section']=request.passengers[i].section
                            isReserved = True
                            break
            elif not(request.passengers[i].section is None or request.passengers[i].section == ''):
                response['passengers'][i]['seat']=request.passengers[i].seat
                response['passengers'][i]['section']=request.passengers[i].section
                isReserved = True 
            if not isReserved:
                if None in self.seat_db['A']:
                    for j in range(len(self.seat_db['A'])):
                        if self.seat_db['A'][j] is None:
                            response['passengers'][i]['seat'] = j+1
                            response['passengers'][i]['section']="A"
                            break
                else:
                    for j in range(len(self.seat_db['B'])):
                        if self.seat_db['B'][j] is None:
                            response['passengers'][i]['seat'] = j+1
                            response['passengers'][i]['section']="B"
                            break
            self.seat_db[response['passengers'][i]['section']][response['passengers'][i]['seat']-1]=self.ticket_counter
        response['status'] = "Confirmed"
        response['ticket_no'] = self.ticket_counter
        self.ticket_db.update({response['ticket_no']:response})
        print("Seat_DB",self.seat_db)
        print("Ticket_DB",self.ticket_db)
        return pb2.ReservationResponse(**response)

        
    def ModifyTicket(self, request, context):

        # get the string from the incoming request
        print(request)
        from_code = request.from_code
        response = self.ticket_db[request.ticket_no].copy()
        for i in range(response['passenger_count']):
            if self.seat_db[request.passengers[i].section][request.passengers[i].seat-1] != request.ticket_no:
                if self.seat_db[request.passengers[i].section][request.passengers[i].seat-1] is not None:
                    response['status'] = 'Failed! The seat is already booked!'
                else:
                    self.seat_db[self.ticket_db[request.ticket_no]['passengers'][i]['section']][self.ticket_db[request.ticket_no]['passengers'][i]['seat']-1] = None
                    # print("REquest: ",self.seat_db[self.ticket_db[request.ticket_no]['passengers'][i]['section']][self.ticket_db[request.ticket_no]['passengers'][i]['seat']-1],self.ticket_db[request.ticket_no]['passengers'][i]['section'],self.ticket_db[request.ticket_no]['passengers'][i]['seat'])
                    self.seat_db[request.passengers[i].section][request.passengers[i].seat-1] = request.ticket_no
                    response['status'] = 'Success! The seat(s) are booked!'
            response['passengers'][i]['section'] = request.passengers[i].section
            response['passengers'][i]['seat'] = request.passengers[i].seat
        
        if response['status'] == 'Success! The seat(s) are booked!':
            self.ticket_db[request.ticket_no] = response
        print("Seat_DB",self.seat_db)
        print("Ticket_DB",self.ticket_db)
        # print("Response: ",response)
        return pb2.ReservationResponse(**response)


    def CancelTicket(self, request, context):
        print(request)
        self.ticket_db[request.ticket_no]['status'] = 'Cancelled'
        for i in range(self.ticket_db[request.ticket_no]['passenger_count']):
            self.seat_db[self.ticket_db[request.ticket_no]['passengers'][i]['section']][self.ticket_db[request.ticket_no]['passengers'][i]['seat']-1] = None
            self.ticket_db[request.ticket_no]['passengers'][i]['section'] = None
            self.ticket_db[request.ticket_no]['passengers'][i]['seat'] = None
        response = self.ticket_db[request.ticket_no]
        print("Seat_DB",self.seat_db)
        print("Ticket_DB",self.ticket_db)
        # print(self.ticket_db)
        return pb2.ReservationResponse(**response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TicketReservationServicer_to_server(TicketReservationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()