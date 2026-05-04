def voice_mode():
    """
    Premium SOC Voice Assistant
    Online Mode  = SOC routing first → AI fallback
    Offline Mode = SOC Menu command execution (continuous)
    """

    try:
        import sounddevice as sd
        import speech_recognition as sr
        import audioop
        import pyttsx3
        import time

        from rich.console import Console
        from rich.panel import Panel
        from rich.live import Live

        from ai.brain import ask_ai

        console = Console()
        recognizer = sr.Recognizer()

        # ==========================================
        # JARVIS VOICE ENGINE
        # ==========================================
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)

        def speak(text):
            try:
                engine.say(text)
                engine.runAndWait()
            except:
                pass

        # ==========================================
        # OFFLINE ROUTER
        # ==========================================
        def run_offline(command):

            command = command.lower()

            def match(words):
                return any(w in command for w in words)

            if match(["help", "help center", "documentation"]):
                from main import help_center
                help_center()

            elif match(["security", "analysis", "audit", "system scan"]):
                from main import analysis_engine
                analysis_engine()

            elif match(["threat", "malware", "cve"]):
                from main import threat_engine
                threat_engine()

            elif match(["incident", "response", "block ip"]):
                from main import incident_toolkit
                incident_toolkit()

            elif match(["forensic", "forensics", "investigation"]):
                from main import forensics_suite
                forensics_suite()

            elif match(["system", "admin", "firewall", "users"]):
                from main import system_admin
                system_admin()

            elif match(["report", "export"]):
                from main import reporting
                reporting()

            elif match(["maintenance", "health"]):
                from main import auto_heal, format_autonomous_report, render_output
                result = auto_heal()
                render_output("AUTONOMOUS MODE", format_autonomous_report(result))

            elif match(["clear"]):
                from main import clear, banner, menu, status_bar
                clear()
                banner()
                menu()
                status_bar()

            elif match(["remote", "scan host"]):
                from main import remote_assessment
                remote_assessment()

            elif "exit" in command:
                return "exit"

            else:
                console.print("[cyan]🧠 SOC AI interpreting command...[/cyan]")

                response = ask_ai(f"""
You are a SOC AI router.

User command:
{command}

Map it to the best SOC module and suggest action.
""")

                console.print(
                    Panel(response, title="AI ROUTER", border_style="green")
                )

            return "ok"

        # ==========================================
        # MODE SELECTOR
        # ==========================================
        console.print(
            Panel.fit(
                "[bold cyan]🎤 SOC VOICE COMMAND CENTER[/bold cyan]\n\n"
                "1. Online JARVIS Mode\n"
                "2. Offline SOC Mode",
                border_style="cyan"
            )
        )

        mode = input("Select Mode [1/2]: ").strip()

        # ==========================================
        # MIC SETUP
        # ==========================================
        try:
            devices = sd.query_devices()
            for i, d in enumerate(devices):
                if d["max_input_channels"] > 0:
                    sd.default.device = (i, None)
                    break
        except:
            pass

        # ==========================================
        # JARVIS GREETING
        # ==========================================
        if mode == "1":
            speak("Jarvis online. SOC systems are active.")

        samplerate = 16000
        duration = 5
        chunk = 1024

        # ==========================================
        # MAIN LOOP
        # ==========================================
        while True:

            console.print(
                Panel.fit(
                    "[bold green]🎤 Listening...[/bold green]\nSay: exit voice mode",
                    border_style="green"
                )
            )

            frames = []
            loops = int((samplerate * duration) / chunk)

            with Live(console=console, refresh_per_second=60) as live:
                stream = sd.RawInputStream(
                    samplerate=samplerate,
                    blocksize=chunk,
                    dtype="int16",
                    channels=1
                )

                with stream:
                    for _ in range(loops):
                        data, _ = stream.read(chunk)
                        frames.append(data)

                        rms = audioop.rms(data, 2)
                        meter = "█" * int(min(rms / 250, 30)) + "░" * (30 - int(min(rms / 250, 30)))

                        live.update(
                            Panel.fit(
                                f"🎙 VOICE LEVEL\n\n{meter}\nInput: {rms}",
                                title="MIC MONITOR",
                                border_style="cyan"
                            )
                        )

                        time.sleep(0.01)

            audio = sr.AudioData(b"".join(frames), samplerate, 2)

            try:
                command = recognizer.recognize_google(audio)
            except:
                command = ""

            command = command.lower().strip()

            if not command:
                continue

            console.print(f"[green]COMMAND:[/green] {command}")

            # ==========================================
            # 🔥 GLOBAL EXIT (HIGHEST PRIORITY)
            # ==========================================
            if "exit voice mode" in command or "stop voice" in command or command == "exit":
                speak("Exiting voice assistant mode.")
                console.print("[red]Voice mode exited.[/red]")
                return "VOICE_EXIT"

            if command == "exit system" or command == "quit system":
                speak("Shutting down system.")
                return "SYSTEM_EXIT"
            # ==========================================
            # SWITCH TO AI MODE
            # ==========================================
            if "switch to ai" in command or "ai assistant" in command:
                from main import ai_chat_mode
                speak("Switching to SOC AI assistant.")
                ai_chat_mode()
                continue

            # ==========================================
            # ONLINE MODE (FIXED ROUTING FIRST)
            # ==========================================
            if mode == "1":

                # STEP 1: LOCAL SOC ROUTING FIRST
                def route_local(cmd):
                    cmd = cmd.lower()

                    def match(words):
                        return any(w in cmd for w in words)

                    if match(["help", "help center", "documentation"]):
                        from main import help_center
                        help_center()
                        return True

                    elif match(["security", "analysis", "audit", "system scan"]):
                        from main import analysis_engine
                        analysis_engine()
                        return True

                    elif match(["threat", "malware", "cve"]):
                        from main import threat_engine
                        threat_engine()
                        return True

                    elif match(["incident", "response", "block ip"]):
                        from main import incident_toolkit
                        incident_toolkit()
                        return True

                    elif match(["forensic", "forensics", "investigation"]):
                        from main import forensics_suite
                        forensics_suite()
                        return True

                    elif match(["system", "system administration", "admin", "firewall", "users"]):
                        from main import system_admin
                        system_admin()
                        return True

                    elif match(["report", "export"]):
                        from main import reporting
                        reporting()
                        return True

                    elif match(["maintenance", "health"]):
                        from main import auto_heal, format_autonomous_report, render_output
                        result = auto_heal()
                        render_output("AUTONOMOUS MODE", format_autonomous_report(result))
                        return True

                    elif match(["remote", "scan host"]):
                        from main import remote_assessment
                        remote_assessment()
                        return True

                    return False

                # STEP 2: TRY LOCAL EXECUTION FIRST
                if route_local(command):
                    continue

                # STEP 3: ONLY IF NOT LOCAL → AI
                analysis = ask_ai(f"""
You are a SOC routing system.

Analyze:
{command}

Return SOC category or GENERAL.
""")

                response = ask_ai(f"""
You are JARVIS SOC assistant.

Routing:
{analysis}

User:
{command}

Respond naturally and professionally.
""")

                console.print(Panel(response, title="JARVIS", border_style="green"))
                speak(response)
                continue

            # ==========================================
            # OFFLINE MODE
            # ==========================================
            result = run_offline(command)

            if result == "exit":
                return

    except Exception as e:
        print(f"Voice module error: {type(e).__name__}: {e}")

