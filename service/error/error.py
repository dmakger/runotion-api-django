from rest_framework import status as st
from rest_framework.response import Response


class ErrorHelper:
    NOT_FOUND = st.HTTP_404_NOT_FOUND
    NOT_CONTENT = st.HTTP_204_NO_CONTENT
    FORBIDDEN = st.HTTP_403_FORBIDDEN

    @staticmethod
    def get_error(error: str, status: int):
        return Response(
            {'error': error},
            status=status,
        )

    def forbidden(self):
        return self.get_error(error="У вас нет доступа", status=self.FORBIDDEN)