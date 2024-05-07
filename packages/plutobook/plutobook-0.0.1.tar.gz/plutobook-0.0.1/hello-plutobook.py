import plutobook
import cairo

margins = plutobook.PageMargins(70, 9, 9, 0)
print(margins)

size = plutobook.PageSize(150, 150)
size.width+=100009
print(size)

print(dir(plutobook))

book = plutobook.Book()
print(dir(book))
print(book.get_viewport_width())
