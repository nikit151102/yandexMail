from uuid import UUID

def get_promo_template_zero_prices(id: UUID):
    return "Подготовьте отчетную документацию!" , f"""
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); padding: 25px; font-size: 16px;">
                <!-- Заголовок -->
                <div style="text-align: center; margin-bottom: 25px;">
                    <h1 style="font-size: 24px; color: #333; font-weight: 600; margin-bottom: 10px;">Добрый день, Уважаемые Друзья!</h1>
                    <p style="font-size: 18px; color: #666; margin: 0; text-align: left;">Наша команда занимается автоматизированной подготовкой документов в сфере капитального ремонта многоквартирных домов.</p>
                    <p style="font-size: 18px; color: #666; margin-top: 10px; text-align: left;">Предлагаем вам в течение нескольких минут подготовить все необходимые документы для сдачи выполненных работ заказчику.</p>
                </div>

                <!-- Основной контент -->
                <div style="margin-bottom: 30px; text-align: left;">
                    <p style="font-size: 20px; margin-bottom: 15px; color: #333; font-weight: 600; text-align: center;">В данный момент Вы можете сформировать свои документы за наш счет!</p>
                    <p style="font-size: 18px; color: #666; margin-bottom: 15px; text-align: center;">В ближайший месяц для новых пользователей будет актуален следующий прайс-лист:</p>
                    <ul style="list-style-type: none; padding-left: 0; margin-bottom: 20px;">
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Сопоставительная ведомость:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">4500₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Акты освидетельствования скрытых работ:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">8500₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Спецификация на материалы:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Ведомость объёмов работ:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Общий журнал работ:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">6700₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Акты гидравлических испытаний:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Акт проверки стяжки:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Акт пролива кровли:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span style="font-size: 16px; color: #333;">Акт прочистки магистралей:</span> 
                            <span style="text-decoration: line-through; color: #888; font-size: 16px;">1150₽</span> 
                            <span style="color: green; font-weight: bold; font-size: 16px;">0₽</span>
                        </li>
                    </ul>
                <!-- Блок кнопки перехода -->
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://rebuildpro.ru" 
                    style="display: inline-block; 
                            background-color: #007BFF; /* Основной синий цвет */
                            color: #fff; 
                            font-size: 16px; 
                            padding: 12px 25px; 
                            text-decoration: none; 
                            border-radius: 8px; 
                            transition: background-color 0.3s ease, transform 0.3s ease;" 
                    onmouseover="this.style.backgroundColor='#0056b3'; this.style.transform='scale(1.05)';" 
                    onmouseout="this.style.backgroundColor='#007BFF'; this.style.transform='scale(1)';">
                    Сформировать документы!
                    </a>
                </div>

                    <p style="font-size: 16px; color: #666; margin-bottom: 15px;">Вы можете качественно и быстро сформировать нужные вам документы, загрузив всего пару файлов.</p>
                    <p style="font-size: 16px; color: #666; margin-bottom: 15px;">Наша команда готова выполнить работу по разработке ИД (документов, которых пока нет на сервисе) вручную. Быстро и качественно сформируем для вас полный комплект документов.</p>
                    <p style="font-size: 16px; color: #333; font-weight: 600; margin-bottom: 15px;">Служба поддержки сервиса работает круглосуточно без перерывов и выходных! Обращайтесь по любым вопросам, будем рады помочь!</p>
                </div>

                <!-- Блок отписки -->
                <div style="text-align: center; margin-top: 30px;">
                    <p style="font-size: 16px; color: #666; margin-bottom: 10px;">Если Вы больше не хотите получать наши письма, Вы можете отписаться:</p>
                    <a href="https://rebuildpro.ru/unsubscribe/{id}" style="display: inline-block; background-color: #ff5722; color: #fff; font-size: 16px; padding: 8px 10px; text-decoration: none; border-radius: 8px; transition: background-color 0.3s ease;" onmouseover="this.style.backgroundColor='#e64a19';" onmouseout="this.style.backgroundColor='#ff5722';">Отписаться от рассылки</a>
                </div>

                <!-- Подвал -->
                <div style="margin-top: 30px; font-size: 14px; color: #777; text-align: center;">
                    <p style="margin-bottom: 5px;">Спасибо, что остаетесь с нами!</p>
                    <p style="margin-bottom: 5px;">С уважением к Вам и Вашему бизнесу, Команда РебилдПро!</p>
                <p style="margin-bottom: 5px;">Наш телефон: +7(915)048-3399</p>
                <p style="margin: 0;">Почтовый адрес: Rebuild-Pro@yandex.ru</p>
                </div>
            </div>
        """
