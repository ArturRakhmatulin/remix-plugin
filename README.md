# remix-plugin
This uses lerna to deploy all the packages with a new version
// SPDX-License-Identifier: GPL-3.0
//Указание версии языка
pragma solidity 0.7.6;

//Начало контракта
contract DPS {
    //Структура водитель
    struct Driver {
        string name; //ФИО
        bool have_lic; //Имеет ли удостоверение
        uint lic; //Номер удостоверения
        uint exp; //Водительский стаж
    }
    
    //Структура транспортное средство
    struct Veh {
        uint categ; //Категория
        uint price; //Рыночная стоимость
        uint time; //Время эксплуатации
    }
    
    //Структура удостоверение
    struct Lic {
        uint validity; //Срок действия
        bool categA; //Категория A
        bool categB; //Категория B
        bool categC; //Категория C
        address payable driver; //Адрес владельца
    }
    
    mapping(address => uint) roles; //Адресу соответствует номер роли (0 - не зарегистрированный, 1 - сотрудник, 2 - водитель)
    mapping(address => Veh) vehs; //Адресу соответствует транспортное средство
    mapping(address => Driver) drivers; //Адресу соответствуют данные водителя
    mapping(address => string[]) messages; //Адресу соответствует цепочка сообщений
    mapping(uint => Lic) lics; //Номеру удостоверения соответствуют данные 
    
    //Указание стандартного нулевого адреса для обозначения отсутствия владельца удостоверения
    address payable default_address = 0x0000000000000000000000000000000000000000;
    
    //Модификатор, проверяющий состояние регистрации
    modifier is_reg() {
        require(roles[msg.sender] != 0, "You havn't got account"); //Условие
        //При true выполняется функция, при false выдаётся сообщение об ошибке
        _; //Этой строкой должен оканчиваться модификатор
    }
    
    //Конструктор, функция, выполняющаяся при деплое контракта
    constructor() {
        //Добавление удостоверений в список

        //Удостоверение 000, срок 11.1.2021, категория A, нет владельца
        lics[0] = Lic(1610323200, true, false, false, default_address);
        
        //Удостоверение 111, срок 12.5.2025, категория B, нет владельца
        lics[111] = Lic(1747008000, false, true, false, default_address);
        
        //Удостоверение 222, срок 9.9.2020, категория C, нет владельца
        lics[222] = Lic(1599609600, false, false, true, default_address);
        
        //Удостоверение 333, срок 13.2.2027, категория A, нет владельца
        lics[333] = Lic(1802476800, true, false, false, default_address);
        
        //Удостоверение 444, срок 11.12.2026, категория B, нет владельца
        lics[444] = Lic(1796947200, false, true, false, default_address);
        
        //Удостоверение 555, срок 24.6.2029, категория C, нет владельца
        lics[555] = Lic(1876953600, false, false, true, default_address);
        
        //Удостоверение 666, срок 31.3.2030, категория A, нет владельца
        lics[666] = Lic(1901145600, true, false, false, default_address);
        
        //Добавление ролей и данных начальным аккаунтам

        roles[0x4018B49404795948a5119Dc971725349D8c85f3e] = 1; //Сотрудник Иван
        drivers[0x4018B49404795948a5119Dc971725349D8c85f3e] = Driver("Ivanov Ivan Ivanovich", false, 0, 2);
        
        roles[0x93df0215167EF6Cbc7548E6C1a70B1D02aCAFD73] = 2; //Водитель Семён
        drivers[0x93df0215167EF6Cbc7548E6C1a70B1D02aCAFD73] = Driver("Semenov Semen Semenovich", false, 0, 5);
        
        roles[0xC68D41FA144da24fdCFaC5faC00fEB6E3F060ea2] = 2; //Водитель Пётр
        drivers[0xC68D41FA144da24fdCFaC5faC00fEB6E3F060ea2] = Driver("Petrov Petr Petrovich", false, 0, 10);
    }
    
    //Регистрация
    function registry(string memory name, uint exp) public {
        require(roles[msg.sender] == 0, "You already have account"); //Проверка отсутствия регистрации
        roles[msg.sender] = 2; //Новый пользователь - Водитель
        drivers[msg.sender] = Driver(name, false, 0, exp); //Внесение данных
    }
    
    //Добавление удостоверения
    function reg_license(uint number, uint validity, uint lic_categ) public is_reg {
        //Проверка отсутствия удостоверения у водителя
        if(drivers[msg.sender].have_lic)
        { send_message("Error adding driver's license: You already have a driver's license!", msg.sender); return; }
        //Проверка существования удостоверения в базе
        else if(lics[number].validity == 0)
        { send_message("Error adding driver's license: The license with the specified number does not exist!", msg.sender); return; }
        //Проверка соответствия срока
        else if(lics[number].validity != validity)
        { send_message("Error adding driver's license: Invalid expiration date!", msg.sender); return; }
        //Проверка соответствия категории
        else if((!lics[number].categA || lic_categ != 1) && (!lics[number].categB || lic_categ != 2) && (!lics[number].categC || lic_categ != 3))
        { send_message("Error adding driver's license: Invalid category!", msg.sender); return; }
        //Проверка доступности удостоверения
        else if(lics[number].driver != default_address)
        { send_message("Error adding driver's license: This driver's license is already in use!", msg.sender); return; }
        //Внесение изменений в данные водителя и удостоверения
        drivers[msg.sender].lic = number;
        drivers[msg.sender].have_lic = true;
        lics[number].driver = msg.sender;
    }
    
    //Добавление категории
    function add_category(uint categ) public is_reg {
        //Проверка наличия удостоверения
        if(!drivers[msg.sender].have_lic) { send_message("Error adding driving category: You don't have a driver's license!", msg.sender); return; }
        //Проверка существования категории
        else if(categ <= 0 || categ >= 4) { send_message("Error adding driving category: You have specified a category that does not exist!", msg.sender); return; }
        //Занесение номера удостоверения в переменную для более быстрого обращения
        uint _lic = drivers[msg.sender].lic;
        //Если водитель хочет добавить категорию 1 (A)
        if(categ == 1) {
            //Проверка отсутствия этой категории в удостоверении
            if(lics[_lic].categA)
            { send_message("Error adding driving category: You already have this driving category!", msg.sender); return; }
            //Добавление категории
            lics[_lic].categA = true;
            //Сообщение об успешном добавлении
            send_message("Driving category 'A' has been successfully added to you.", msg.sender);
        }
        //Если водитель хочет добавить категорию 2 (B)
        else if(categ == 2) {
            //Проверка отсутствия этой категории в удостоверении
            if(lics[_lic].categB)
            { send_message("Error adding driving category: You already have this driving category!", msg.sender); return; }
            //Добавление категории
            lics[_lic].categB = true;
            //Сообщение об успешном добавлении
            send_message("Driving category 'B' has been successfully added to you.", msg.sender);
        }
        //Если водитель хочет добавить категорию 3 (C)
        else {
            //Проверка отсутствия этой категории в удостоверении
            if(lics[_lic].categC)
            { send_message("Error adding driving category: You already have this driving category!", msg.sender); return; }
            //Добавление категории
            lics[_lic].categC = true;
            //Сообщение об успешном добавлении
            send_message("Driving category 'C' has been successfully added to you.", msg.sender);
        }
    }
    
    //Продление срока действия удостоверения
    function renewal_license() public is_reg {
        //Проверка наличия удостоверения
        if(!drivers[msg.sender].have_lic) { send_message("Error while renewing driver's license: You don't have a driver's license!", msg.sender); return; }
        //Занесение номера удостоверения в переменную для более быстрого обращения
        uint _lic = drivers[msg.sender].lic;
        //Переменная срока действия
        uint lic_date = lics[_lic].validity;
        //Если больше месяца до окончания и срок ещё не наступил, отправляется ошибка
        if(lic_date - block.timestamp > 2629743 && block.timestamp < lic_date)
        { send_message("Error while renewing driver's license: More than a month before expiration!", msg.sender); }
        //Иначе, новый срок = текущая дата + год, отправляется сообщение об успехе
        else {
            lics[_lic].validity = block.timestamp + 31556926;
            send_message("Driver's license has been successfully renewed.", msg.sender);
        }
    }
    
    //Добавление транспортного средства
    function reg_vehicle(uint categ, uint price, uint time) public is_reg {
        //Занесение номера удостоверения в переменную для более быстрого обращения
        uint _lic = drivers[msg.sender].lic;
        //Проверка наличия удостоверения
        if(!drivers[msg.sender].have_lic)
        { send_message("Error while registering a vehicle: You don't have a driver's license!", msg.sender); return; }
        //Проверка соответствия категории
        else if((!lics[_lic].categA || categ != 1) && (!lics[_lic].categB || categ != 2) && (!lics[_lic].categC || categ != 3))
        { send_message("Error while registering a vehicle: You don't have this driving category!", msg.sender); return; }
        //Добавление транспортного средства водителю
        vehs[msg.sender] = Veh(categ, price, time);
    }
    
    //Получение данных водителя
    function get_driver_info() public view is_reg returns(string memory, uint, uint) {
        return(drivers[msg.sender].name, drivers[msg.sender].lic, drivers[msg.sender].exp);
    }
    
    //Получение данных транспортного средства
    function get_vehicle_info() public view is_reg returns(uint, uint, uint) {
        require(vehs[msg.sender].categ > 0, "You havn't got vehicle");
        return(vehs[msg.sender].categ, vehs[msg.sender].price, vehs[msg.sender].time);
    }
    
    //Получение данных удостоверения
    function get_license_info() public view is_reg returns(uint, bool, bool, bool) {
        require(drivers[msg.sender].have_lic, "You havn't got license");
        uint _lic = drivers[msg.sender].lic;
        return(lics[_lic].validity, lics[_lic].categA, lics[_lic].categB, lics[_lic].categC);
    }
    
    //Отправка сообщения
    function send_message(string memory text, address reciver) private {
        messages[reciver].push(text);
    }
    
    //Получение текста сообщения
    function get_message(uint number) public view is_reg returns(string memory text) {
        return messages[msg.sender][number];
    }
    
    //Получение количества сообщений
    function get_messages() public view is_reg returns(uint count) {
        return messages[msg.sender].length;
    }

    //Получение роли
    function get_role() public view is_reg returns(string memory) {
        return roles[msg.sender] == 1 ? "DPS" : "Driver";
    }
}
