import grpc
import ticket_reservation_pb2_grpc as pb2_grpc
import ticket_reservation_pb2 as pb2


class TicketReservationClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.TicketReservationStub(self.channel)

    def get_url(self, request, option):
        """
        Client function to call the rpc for GetServerResponse
        """
        # print(request)
        message = pb2.ReservationRequest(**request)
        print(f'{message}')
        if option == 1:
            return self.stub.ReserveTicket(message)
        elif option == 2:
            return self.stub.ModifyTicket(message)
        elif option == 3:
            return self.stub.CancelTicket(message)
            


if __name__ == '__main__':
    client = TicketReservationClient()
    option = 0
    while option != 4:
        print("Welcome! Train Ticket Reservation\n\n 1.Reserve Ticket\n 2.Modify Seat Allotment\n 3.Cancel Ticket\n 4.Close\n\nChoose an option: ",end='')
        option = int(input())
        if option == 1:
            print("From: ",end='')
            from_code = input()
            print("To: ",end='')
            to_code = input()
            print("Passenger Count: ",end='')
            passenger_count = int(input())
            passengers=[]
            request = {'from_code':from_code,'to_code':to_code, 'price_paid':passenger_count*20, 'passenger_count':passenger_count}
            for i in range(passenger_count):
                passengers.append({})
                print("Passenger",i+1,"\nFirst Name: ",end='')
                passengers[i]['first_name'] = input()
                print("Last Name: ",end='')
                passengers[i]['last_name'] = input()
                print("Email: ",end='')
                passengers[i]['email'] = input()
                print("Address: ",end='')
                passengers[i]['address'] = input()    
            request.update({"passengers":passengers})
            # request = {'from_code':'tpj','to_code':"cbe", 'price_paid':650, 'passenger_count':2,'passengers':[{'first_name':'Ramanan','last_name':'Sureshkumar','email':'skramana21@gmail.com','address':'Address 1'},{'first_name':'Kalidasan','last_name':'Ramakrishnan','email':'kalisdaseddy@gmail.com','address':'Address 2'}]}
            # request = {'from_code':'tpj','to_code':"cbe", 'price_paid':650, 'passenger_count':2,'passengers':[{'first_name':'Ramanan','last_name':'Sureshkumar','email':'skramana21@gmail.com','address':'Address 1','section':'A','seat':2},{'first_name':'Kalidasan','last_name':'Ramakrishnan','email':'kalisdaseddy@gmail.com','address':'Address 2','section':'B','seat':2}]}
            
            result = client.get_url(request,option)
            print(f'Receipt Received: {result}')
        elif option == 2:
            print("Ticket No: ",end='')
            ticket_no = int(input())
            print("Passenger Count: ",end='')
            passenger_count = int(input())
            passengers=[]
            request = {'ticket_no':ticket_no, 'passenger_count':passenger_count}
            for i in range(passenger_count):
                passengers.append({})
                print("Passenger",i+1,"\nSection: ",end='')
                passengers[i]['section'] = input()
                print("Seat: ",end='')
                passengers[i]['seat'] = int(input())   
            request.update({"passengers":passengers})
            result = client.get_url(request,option)
            print(f'Receipt Received: {result}')
        elif option == 3:
            print("Ticket No: ",end='')
            ticket_no = int(input())
            request = {'ticket_no':ticket_no}
            result = client.get_url(request,option)
            print(f'Receipt Received: {result}')
        elif option == 4:
            exit()
        else:
            print("Incorret Option")