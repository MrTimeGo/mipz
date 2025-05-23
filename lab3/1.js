/*
Запахи коду:
- Довгий метод
- Велика вкладеність умовних операторів


Методи рефакторингу:
- Заміна вкладених умовних операторів граничним оператором
- Заміна умовного оператора на тернарний оператор
- Заміна циклу на метод `reduce`


Також було видалено змінні hasActive та foundInactive, оскільки вони не несли
корисну інформацію і були зайвими.
*/

function processUsers(users, callback) {
  const results = users.reduce((acc, user) => {
    if (!user?.name) {
      return acc;
    }

    if (!acc[user.name]) {
      acc[user.name] = {
        count: 1,
        status: user.active ? "active" : "inactive",
      };
    } else {
      acc[user.name].count++;
    }

    return acc;
  }, {});

  callback(results);
}

processUsers(
  [
    { name: "John", active: true },
    { name: "Jane", active: false },
    { name: "Jim", active: true },
  ],
  console.log
);
