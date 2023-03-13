from rest_framework.response import Response
from rest_framework import status, generics
from .models import NoteModel
from .serializers import NoteSerializer
import math

class Notes(generics.GenericAPIView):
    serializer_class = NoteSerializer
    queryset = NoteModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        notes = NoteModel.objects.all()
        total_notes = notes.count()
        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_num:end_num], many=True)
        context = {
            "status": "success",
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        }
        return Response(context)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"status": "success", "note": serializer.data}
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {"status": "fail", "message": serializer.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        

class NoteDetail(generics.GenericAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer

    def get_note(self, pk):
        try:
            return NoteModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        note = self.get_note(pk=pk)
        if note == None:
            context = {"status": "fail", "message": f"Note with Id: {pk} not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(note)
        context = {"status": "success", "note": serializer.data}
        return Response(context)

    def patch(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            context = {"status": "fail", "message": f"Note with Id: {pk} not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {"status": "success", "note": serializer.data}
            return Response(context)
        context = {"status": "fail", "message": serializer.errors}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            context = {"status": "fail", "message": f"Note with Id: {pk} not found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)