graph TD

Start(("شروع")) --> LoadIO[/"پروفایل را بارگذاری کن profile.json"/]

LoadIO --> InitCart["مقدار اولیه سبد خرید را برابر با خالی قرار بده"]

InitCart --> ShowMenu["منوی اصلی را نمایش بده"]

ShowMenu --> LoopCond{"آیا پنجره باز است؟"}

  

LoopCond -->|خیر| End(("پایان"))

  

LoopCond -->|بله| WaitEvent[/"رویداد را از کاربر دریافت کن (کلیک، جستجو، ...)"/]

WaitEvent --> ActionDec{"بررسی کن نوع رویداد چیست؟"}

  

ActionDec -->|افزودن غذا| AddProc["ایتم را به سبد خرید اضافه کن یا افزایش بده"]

AddProc --> UpdateUI["شمارنده در منو را بروزرسانی کن"]

UpdateUI --> NotifyIO[/"نمایش بده که غذا به منو اضافه شده است"/]

NotifyIO --> LoopCond

  

ActionDec -->|کاهش تعداد| DecProc["تعداد را کاهش بده یا از سبد حذف کن"]

DecProc --> UpdateUI2["شمارنده در منو را بروزرسانی کن"]

UpdateUI2 --> LoopCond

  

ActionDec -->|مشاهده سبد| OpenCart["بخش سبد خرید را باز کن"]

OpenCart --> CartAction{"عملیات در سبد چیست؟"}

  

CartAction -->|تغییر تعداد| ChangeQty["تعداد ایتم را بروزرسانی کن"]

ChangeQty --> RefreshCart["نمایش سبد خرید را بازخوانی کن"]

RefreshCart --> CartAction

  

CartAction -->|حذف آیتم| RemoveItem["آیتم را از سبد حذف کن"]

RemoveItem --> RefreshCart

  

CartAction -->|پاک کردن سبد| ClearConfirm{"برای کاربر یک هشدار چاپ کن که آیا از حذف اطمینان دارد؟"}

ClearConfirm -->|بله| ClearCart["ایتم هارا حذف کن"]

ClearConfirm -->|خیر| CartAction

ClearCart --> RefreshCart

  

CartAction -->|تکمیل سفارش| CheckProfile{"بررسی کن آیا اطلاعات پروفایل وارد شده؟<br/>(نام، تلفن، آدرس)"}

CheckProfile -->|خیر| WarnIO[/"هشدار<اعلان> را چاپ کن : لطفا پروفایل را تکمیل کنید"/]

WarnIO --> CartAction

  

CheckProfile -->|بله| ShowTotalIO[/"جمع کل راچاپ کن و برای کاربر صفحه تایید را چاپ کن و منتظر جواب او باش"/]

ShowTotalIO --> ConfirmOrder{"هشدار<اعلان> را چاپ کن: آیا اطمینان دارید؟"}

ConfirmOrder -->|خیر| CartAction

ConfirmOrder -->|بله| TryExport["فاکتور را در فرمت فایل اکسل خروجی بگیر"]

TryExport --> CheckExcel{"openpyxl بررسی کن کتابخوانه مورد نظر نصب باشد"}

CheckExcel -->|بله| CreateExcel[("فایل اکسل با تاریخ جلالی را ایجاد کن")]

CheckExcel -->|خیر| ErrorIO[/ هشدار<اعلان> را چاپ کن : کتابخانه نصب نیست"/]

CreateExcel --> ClearClose["سبد را پاک کن و دیالوگ را ببند"]

ErrorIO --> ClearClose

ClearClose --> LoopCond

  

ActionDec -->|ویرایش پروفایل| OpenProf["دیالوگ پروفایل را باز کن"]

OpenProf --> ProfAction{"بررسی کن عملیات پروفایل چیست؟"}

  

ProfAction -->|آپلود تصویر| UploadIO[/"فایل تصویر را انتخاب کن و پیش نمایش را نشان بده"/]

UploadIO --> ProfAction

  

ProfAction -->|حذف تصویر| RemoveImg["مسیر تصویر را پاک کن و تصویر را بروزرسانی کن"]

RemoveImg --> ProfAction

  

ProfAction -->|ذخیره| SaveProf["داده هارا در پروفایل ذخیره بکن"]

SaveProf --> StoreProf[(" اطلاعات پروفایل ذخیره کن")]

StoreProf --> UpdateAvatar["دکمه آواتار را بروزرسانی کن"]

UpdateAvatar --> LoopCond

  

ProfAction -->|انصراف| LoopCond

  

ActionDec -->|جستجو یا انتخاب دسته| FilterProc["فیلتر جست و جو را اعمال کن و ایتم های تطبیقی را نمایش بده"]

FilterProc --> LoopCond

  

ActionDec -->|بستن پنجره| CloseWin["وضعیت پنجره را از باز به بسته تغییر بده"]

CloseWin --> LoopCond