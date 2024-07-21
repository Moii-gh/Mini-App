#include <iostream>
#include <fstream>
#include <windows.h> 
#include <string>
#include <cstring>

using namespace std;

const int MAX_DELO = 100; // Максимальное количество дел
const char* filename = "delo.txt"; // Имя файла для сохранения и загрузки

struct delo
{
    char name[256];
    int prior;
    char ops[1024];
    char date[11]; // Формат даты ДД/ММ/1ГГГГ
};

void inputDelo(delo& d)
{
    cout << "Введите название задания: "; cin >> d.name;
    cout << "Введите приоритет задания (от 1 до 10 где 1 наивысший приоритет!):"; cin >> d.prior;
    cout << "Введите описание задания: "; cin >> d.ops;
    cout << "Введите дату задания в формате день/неделя/месяц "; cin >> d.date;
}

void saveDeloToFile(const delo* mas, int size, const char* filename)
{
    ofstream file(filename);
    if (!file.is_open())
    {
        cout << "Не удалось открыть файл для записи." << endl;
        return;
    }

    for (int i = 0; i < size; ++i)
    {
        if (strlen(mas[i].name) > 0) // Проверяем, что имя не пустое
        {
            file << mas[i].name << " " << mas[i].prior << " " << mas[i].ops << " " << mas[i].date << "\n";
        }
    }

    file.close();
    cout << "Задания успешно сохранены в файл " << filename << endl;
}

void loadDeloFromFile(delo* mas, int& size, const char* filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "Не удалось открыть файл для чтения." << endl;
        return;
    }

    size = 0; // Сброс текущего размера массива
    while (file >> mas[size].name >> mas[size].prior >> mas[size].ops >> mas[size].date)
    {
        size++;
    }

    file.close();
}

void deleteDeloFromFile(const char* filename, int index)
{
    delo tempDelos[MAX_DELO];
    int tempSize = 0;
    ifstream fileIn(filename);
    int currentIndex = 0;

    if (!fileIn.is_open())
    {
        cout << "Не удалось открыть файл для чтения." << endl;
        return;
    }

    // Чтение всех задач из файла во временный массив, кроме удаляемой
    while (fileIn >> tempDelos[tempSize].name >> tempDelos[tempSize].prior >> tempDelos[tempSize].ops >> tempDelos[tempSize].date)
    {
        if (currentIndex != index)
        {
            tempSize++;
        }
        currentIndex++;
    }
    fileIn.close();

    // Перезапись файла без удаленной задачи
    ofstream fileOut(filename);
    if (!fileOut.is_open())
    {
        cout << "Не удалось открыть файл для записи." << endl;
        return;
    }

    for (int i = 0; i < tempSize; ++i)
    {
        fileOut << tempDelos[i].name << " " << tempDelos[i].prior << " " << tempDelos[i].ops << " " << tempDelos[i].date << "\n";
    }
    fileOut.close();
}

void outputDelo(const delo* mas, int size)
{
    for (int i = 0; i < size; ++i)
    {
        if (strlen(mas[i].name) > 0) // Проверяем, что имя не пустое
        {
            cout << "Задание: " << mas[i].name << ", Приоритет: " << mas[i].prior
                << ", Описание: " << mas[i].ops << ", Дата: " << mas[i].date << endl;
        }
    }
}

void editDelo(delo* mas, int size)
{
    int index;
    cout << "Введите индекс задания для редактирования: ";
    cin >> index;
    if (index >= 0 && index < size)
    {
        cout << "Введите новое название задания: "; cin >> mas[index].name;
        cout << "Введите новый приоритет задания: "; cin >> mas[index].prior;
        cout << "Введите новое описание задания: "; cin >> mas[index].ops;
        cout << "Введите новую дату задания: "; cin >> mas[index].date;
    }
    else
    {
        cout << "Задание с таким индексом не найдено." << endl;
    }
}

void findDelo(const delo* mas, int size)
{
    char searchName[256];
    cout << "Введите имя задания для поиска: ";
    cin >> searchName;
    for (int i = 0; i < size; ++i)
    {
        if (strcmp(mas[i].name, searchName) == 0)
        {
            cout << "Задание найдено: " << mas[i].name << ", Приоритет: " << mas[i].prior
                << ", Описание: " << mas[i].ops << ", Дата: " << mas[i].date << endl;
            return;
        }
    }
    cout << "Задание с таким именем не найдено." << endl;
}

void sortDelo(delo* mas, int size)
{
    for (int i = 0; i < size - 1; ++i)
    {
        for (int j = 0; j < size - i - 1; ++j)
        {
            if (mas[j].prior > mas[j + 1].prior)
            {
                delo temp = mas[j];
                mas[j] = mas[j + 1];
                mas[j + 1] = temp;
            }
        }
    }
}

int main()
{
    setlocale(LC_ALL, "RU");

    delo deloArray[MAX_DELO]; // Массив для хранения дел
    int currentSize = 0; // Текущее количество дел в массиве

    int menu = -1;
    do
    {
        cout << "MENU" << endl;
        cout << "1 - Ввести новую задачу;" << endl;
        cout << "2 - Удалить задачу;" << endl;
        cout << "3 - Редактировать задание;" << endl;
        cout << "4 - Найти задание;" << endl;
        cout << "5 - Вывести на экран задания;" << endl;
        cout << "6 - Отсортировать задания;" << endl;
        cout << "7 - Сохранить задания в файл;" << endl;
        cout << "0 - Выход;" << endl;
        cout << "Выберите пункт меню: ";
        cin >> menu;
        system("cls");

        switch (menu)
        {
        case 1:
            if (currentSize < MAX_DELO)
            {
                inputDelo(deloArray[currentSize]);
                currentSize++;
            }
            else
            {
                cout << "Достигнуто максимальное количество задач." << endl;
            }
            break;
        case 2:
            int indexToDelete;
            cout << "Введите индекс задачи для удаления: ";
            cin >> indexToDelete;
            deleteDeloFromFile(filename, indexToDelete);
            break;
            break;
        case 3:
            editDelo(deloArray, currentSize);
            break;
        case 4:
            findDelo(deloArray, currentSize);
            break;
        case 5:
            loadDeloFromFile(deloArray, currentSize, filename);
            outputDelo(deloArray, currentSize);
            break;
            break;
        case 6:
            sortDelo(deloArray, currentSize);
            cout << "Задания отсортированы по приоритету." << endl;
            break;
        case 7:
            saveDeloToFile(deloArray, currentSize, filename);
            break;
            break;
        }
    } while (menu != 0);

    return 0;
}
