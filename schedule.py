from  heap import MinHeap

def assign_rooms(appointments):

    ordered = sorted(appointments, key=lambda a: (a.start_minutes, a.id))

    heap = MinHeap()
    rooms_by_id = {}
    total_rooms = 0

    for appointment in ordered:
        end = appointment.end_minutes

        if len(heap) > 0 and heap.peek()[0] <= appointment.start_minutes:
            room = heap.peek()[1]
            heap.replace_top((end, room))
        else:
            total_rooms += 1
            room = total_rooms
            heap.push((end, room))

        rooms_by_id[appointment.id] = room

    return rooms_by_id, total_rooms