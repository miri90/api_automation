from datetime import datetime


class GetFunUtil:
    @staticmethod
    def get_fun_date(prefix=None):
        if prefix is None:
            prefix="auto_"
        now=datetime.now()
        s=f"{prefix}{now.year}{now.month}{now.day}{now.hour}{now.minute}"

        return s

if __name__=="__main__":
    GetFunUtil.get_fun_date()