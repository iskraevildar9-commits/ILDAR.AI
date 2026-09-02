from flask import Flask, render_template_string, request, jsonify
import datetime

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ILDAR.AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        
        body { 
            background: linear-gradient(135deg, #0f0c20, #15102a, #060411); 
            color: #ffffff; 
            min-height: 100vh;
            display: flex; 
            justify-content: center; 
            align-items: center;
            padding: 15px;
        }

        .chat-container { 
            width: 100%; 
            max-width: 480px; 
            height: 90vh;
            max-height: 700px;
            background: rgba(25, 20, 45, 0.6); 
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 24px; 
            padding: 20px; 
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(138, 43, 226, 0.2);
        }

        .header {
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 15px;
        }

        .header h1 { 
            font-size: 22px; 
            font-weight: 700;
            background: linear-gradient(90deg, #00f2fe, #4facfe, #00ff87);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1px;
        }

        .status {
            font-size: 11px;
            color: #00ff87;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 4px;
            font-weight: 600;
        }

        #chat { 
            flex: 1; 
            overflow-y: auto; 
            padding-right: 5px;
            margin-bottom: 15px; 
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        /* Стиль полосы прокрутки */
        #chat::-webkit-scrollbar { width: 4px; }
        #chat::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }

        .msg-wrapper {
            display: flex;
            flex-direction: column;
            max-width: 82%;
        }

        .msg-wrapper.user {
            align-self: flex-end;
            align-items: flex-end;
        }

        .msg-wrapper.bot {
            align-self: flex-start;
            align-items: flex-start;
        }

        .sender-name {
            font-size: 10px;
            color: rgba(255, 255, 255, 0.4);
            margin-bottom: 4px;
            padding: 0 4px;
        }

        .msg { 
            padding: 12px 16px; 
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.5;
            word-break: break-word;
        }

        .user .msg { 
            background: linear-gradient(135deg, #0052d4, #4364f7, #6fb1fc); 
            color: #fff; 
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 15px rgba(67, 100, 247, 0.3);
        }

        .bot .msg { 
            background: rgba(255, 255, 255, 0.07); 
            color: #e2e8f0; 
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom-left-radius: 4px;
            backdrop-filter: blur(10px);
        }

        .controls {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .input-group { 
            display: flex; 
            gap: 10px; 
            background: rgba(0, 0, 0, 0.3);
            padding: 6px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        input { 
            flex: 1; 
            padding: 12px 16px; 
            background: transparent; 
            color: #fff; 
            border: none; 
            outline: none;
            font-size: 14px; 
        }

        input::placeholder { color: rgba(255, 255, 255, 0.3); }

        .send-btn { 
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #00f2fe, #4facfe); 
            color: #000; 
            border: none; 
            border-radius: 12px;
            font-weight: bold; 
            cursor: pointer; 
            display: flex;
            justify-content: center;
            align-items: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(79, 172, 254, 0.4);
        }

        .voice-btn { 
            width: 100%; 
            padding: 14px; 
            background: linear-gradient(135deg, #7F00FF, #E100FF); 
            color: #fff; 
            border: none; 
            font-weight: 600; 
            font-size: 14px;
            cursor: pointer; 
            border-radius: 16px; 
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            box-shadow: 0 6px 20px rgba(225, 0, 255, 0.3);
            transition: all 0.2s ease;
        }

        .voice-btn:hover {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(225, 0, 255, 0.4);
        }

        .voice-btn:active {
            transform: translateY(1px);
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>ILDAR.AI</h1>
            <div class="status">● Voice Assistant Ready</div>
        </div>
        <div id="chat">
            <div class="msg-wrapper bot">
                <span class="sender-name">ILDAR.AI</span>
                <div class="msg">Привет! Я твой голосовой ассистент. Задай мне вопрос или попроси рассказать шутку!</div>
            </div>
        </div>
        <div class="controls">
            <div class="input-group">
                <input type="text" id="userInput" placeholder="Напиши или скажи..." onkeydown="if(event.key==='Enter') send()">
                <button class="send-btn" onclick="send()">➔</button>
            </div>
            <button class="voice-btn" onclick="startVoice()">🎤 Сказать голосом</button>
        </div>
    </div>

    <script>
        function speakBotResponse(text) {
            let cleanText = text.replace(/<br\s*\/?>/gi, " "); 
            
            let utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'ru-RU';
            utterance.rate = 1.0; 
            
            window.speechSynthesis.cancel(); 
            window.speechSynthesis.speak(utterance);
        }

        async function send(customText = null) {
            let input = document.getElementById("userInput");
            let text = customText || input.value.trim();
            if (!text) return;

            let chat = document.getElementById("chat");
            
            // Сообщение пользователя
            chat.innerHTML += `
                <div class='msg-wrapper user'>
                    <span class='sender-name'>Ты</span>
                    <div class='msg'>${text}</div>
                </div>`;
            
            if (!customText) input.value = "";
            chat.scrollTop = chat.scrollHeight;

            let res = await fetch("/api", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: text })
            });
            let data = await res.json();
            
            // Ответ бота
            chat.innerHTML += `
                <div class='msg-wrapper bot'>
                    <span class='sender-name'>ILDAR.AI</span>
                    <div class='msg'>${data.reply}</div>
                </div>`;
            chat.scrollTop = chat.scrollHeight;

            speakBotResponse(data.reply);
        }

        function startVoice() {
            window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!window.SpeechRecognition) {
                alert("Ваш браузер не поддерживает голосовой ввод. Используйте Chrome или Safari.");
                return;
            }

            let recognition = new SpeechRecognition();
            recognition.lang = 'ru-RU';
            recognition.start();

            recognition.onresult = function(event) {
                let voiceText = event.results[0][0].transcript;
                document.getElementById("userInput").value = voiceText;
                send(voiceText);
            };
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_CODE)

@app.route("/api", methods=["POST"])
def bot_logic():
    user_input = request.json.get("command", "").lower().strip()
    
    # 1. Википедия про Ильдара
    if any(w in user_input for w in ["википедия", "вики", "расскажи про ильдара", "кто такой ильдар", "история"]):
        reply = (
            "Википедия про Ильдара. "
            "Ильдар, 14 лет — юный разработчик и создатель ILDAR.AI. "
            "Учится в школе №5 с. Чунджа в 9 классе. "
            "С детства увлекался логическими играми и математикой. "
            "Завоевал 1-е место в конкурсе Ақбота по математике и английскому языку. "
            "В 9 классе начал изучать программирование и создал этот проект!"
        )

    # 2. Шутки и Анекдоты
    elif any(w in user_input for w in ["шутка", "анекдот", "пошути", "посмеши"]):
        if any(w in user_input for w in ["школа", "учеба", "урок", "учитель"]):
            reply = "Учитель: 'Ильдар, почему ты опоздал?' — 'Учиться никогда не поздно, профессор!'"
        elif any(w in user_input for w in ["друг", "друзья", "дружба"]):
            reply = "Настоящий друг не спросит 'зачем?', он просто скажет 'я с тобой, погнали!'"
        elif any(w in user_input for w in ["мама", "мам"]):
            reply = "Мама — это единственный человек, который знает, где лежит то, что ты 'точно никуда не перекладывал'."
        elif any(w in user_input for w in ["папа", "пап"]):
            reply = "Папа чинит всё в доме двумя вещами: скотчем и фразой 'и так сойдет!'"
        elif any(w in user_input for w in ["семья", "родители"]):
            reply = "Семья — это когда у всех один пароль от Wi-Fi и одна зарядка на всех!"
        else:
            reply = "Школьник пришел домой: 'Мама, я сегодня получил 5!' — 'Ого, по какому предмету?' — '3 по математике и 2 по физике!'"

    # 3. Стихи и Поэзия
    elif any(w in user_input for w in ["стих", "стихотворение", "поэзия", "прочитай стих"]):
        if any(w in user_input for w in ["школа", "учеба", "урок"]):
            reply = "Звонок звенит, урок идет, <br>В тетради код Ильдар ведет. <br>Школа дает нам путь к мечтам, <br>Учеба — ключ к любым вершинам!"
        elif any(w in user_input for w in ["друг", "друзья"]):
            reply = "Если рядом верный друг, <br>Ярче станет все вокруг! <br>Вместе кодим, вместе чилим, <br>Все вершины мы покорим!"
        elif any(w in user_input for w in ["мама", "мам"]):
            reply = "Мама — свет и доброта, <br>С нею радость навсегда. <br>Согревает теплотой, <br>Самый близкий человек родной!"
        elif any(w in user_input for w in ["папа", "пап"]):
            reply = "Папа мудрый, папа сильный, <br>Он во всем пример стабильный. <br>Все починит, даст совет, <br>Лучше папы в мире нет!"
        elif any(w in user_input for w in ["семья", "родители"]):
            reply = "Семья — наш дом, наш прочный щит, <br>Здесь сердце радостью горит. <br>Любовь, уют и теплый чай, <br>Семью всегда ты уважай!"
        else:
            reply = "Код строчу я день и ночь, <br>Чтобы пользователю помочь. <br>ILDAR.AI всегда с тобой, <br>Твой ассистент и друг цифровой!"

    # 4. Приветствия
    elif any(w in user_input for w in ["привет", "здарова", "салам", "здравствуй", "хай", "хеллоу", "добрый", "здорово", "ку"]):
        reply = "Привет! Как твои дела?"

    # 5. Прощания
    elif any(w in user_input for w in ["пока", "до свидания", "бай", "увидимся", "стоп", "прощай", "покеда"]):
        reply = "До связи! Если что, я всегда тут на сервере."

    # 6. Вопросы про дела
    elif any(phrase in user_input for phrase in ["как дела", "как ты", "шо ты", "как оно", "как жизнь", "как сам"]):
        reply = "Да всё отлично, работаю в штатном режиме! А ты чем занимаешься?"

    # 7. Ответы на вопрос "Чем занимаешься"
    elif any(w in user_input for w in ["программирую", "кожу", "пишу код", "учу питон", "python", "прогу"]):
        reply = "О, уважуха! Программирование — это мощь. Что именно пишешь?"
    elif any(w in user_input for w in ["отдыхаю", "лежу", "чилю", "чилл", "кайфую", "расслабляюсь", "сплю", "валяюсь"]):
        reply = "Красавчик, отдых тоже нужен! Набирайся сил."
    elif any(w in user_input for w in ["учусь", "уроки", "домашка", "школа", "в школе", "учу"]):
        reply = "Учеба — это важно! Главное — не перегружайся."
    elif any(w in user_input for w in ["играю", "катка", "в компик", "игры", "кс", "дота", "майнкрафт"]):
        reply = "О, плотная катка! Желаю легкой победы!"
    elif any(w in user_input for w in ["гуляю", "на улице", "с друзьями", "бегаю", "спорт"]):
        reply = "Отлично проводишь время!"

    # 8. Общее настроение
    elif any(w in user_input for w in ["хорошо", "отлично", "нормально", "супер", "классно", "кайф", "четко"]):
        reply = "Красота! Рад, что у тебя всё на высоте."
    elif any(w in user_input for w in ["плохо", "не очень", "грустно", "устал", "скучно"]):
        reply = "Эх, бывало и лучше... Отдохни немного, всё наладится!"

    # 9. Знакомство и создатель
    elif any(phrase in user_input for phrase in ["как тебя зовут", "кто ты", "твое имя"]):
        reply = "Меня зовут ILDAR.AI!"
    elif any(phrase in user_input for phrase in ["кто тебя создал", "кто твой создатель", "кто тебя сделал", "чей ты"]):
        reply = "Меня создал Ильдар — талантливый разработчик из 9 класса! Напиши или скажи 'википедия', чтобы узнать подробнее."
    elif any(phrase in user_input for phrase in ["сколько тебе лет", "твой возраст"]):
        reply = "Я родился совсем недавно, так что я ещё молодой бот!"

    # 10. Вежливость и эмоции
    elif any(w in user_input for w in ["спасибо", "благодарю", "отдуши", "спас"]):
        reply = "Пожалуйста! Всегда рад помочь."
    elif any(w in user_input for w in ["молодец", "красава", "красавчик", "умница", "топ"]):
        reply = "Стараюсь! Спасибо за похвалу!"
    elif any(w in user_input for w in ["ахах", "хаха", "лол", "смешно"]):
        reply = "Рад, что поднял тебе настроение!"

    # 11. Время и возможности
    elif "что ты умеешь" in user_input:
        reply = "Умею говорить голосом, рассказывать шутки и стихи про школу или семью, знать 'википедию' и считать примеры!"
    elif "время" in user_input:
        now = datetime.datetime.now()
        reply = f"Сейчас: {now.strftime('%H:%M:%S')}"

    # 12. Математика
    elif any(op in user_input for op in ["+", "-", "*", "/"]):
        try:
            allowed = "0123456789+-*/. "
            if all(c in allowed for c in user_input):
                result = eval(user_input)
                reply = f"Результат: {result}"
            else:
                reply = "Я умею считать только простые примеры с числами!"
        except:
            reply = "Не удалось посчитать пример!"

    # 13. Универсальный ответ
    else:
        reply = "Понял тебя! Расскажи ещё что-нибудь, спроси 'кто такой ильдар' или попроси рассказать 'стих про маму'."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
