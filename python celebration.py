#!/usr/bin/env python3
"""
🎆 Happy New Year 2026 Celebration App 🎆
A beautiful animated celebration with fireworks, confetti, and music!
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import math
import time
import colorsys
from datetime import datetime, timedelta
import threading

class Particle:
    """A single particle for fireworks/confetti."""
    def __init__(self, x, y, color, vx, vy, particle_type="firework"):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = 1.0
        self.decay = random.uniform(0.015, 0.03)
        self.size = random.randint(2, 5)
        self.particle_type = particle_type
        self.trail = []
        self.gravity = 0.15 if particle_type == "firework" else 0.05
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-10, 10)

    def update(self):
        """Update particle position and life."""
        # Store trail
        if self.particle_type == "firework" and len(self.trail) < 5:
            self.trail.append((self.x, self.y))
        
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.99
        self.life -= self.decay
        self.rotation += self.rotation_speed
        
        if self.particle_type == "confetti":
            self.vx += random.uniform(-0.2, 0.2)
        
        return self.life > 0

    def draw(self, canvas):
        """Draw the particle on canvas."""
        if self.life <= 0:
            return
        
        alpha = max(0, min(1, self.life))
        size = self.size * alpha
        
        if self.particle_type == "firework":
            # Draw trail
            for i, (tx, ty) in enumerate(self.trail):
                trail_alpha = (i + 1) / len(self.trail) * alpha * 0.5
                trail_size = size * trail_alpha
                if trail_size > 0.5:
                    canvas.create_oval(
                        tx - trail_size, ty - trail_size,
                        tx + trail_size, ty + trail_size,
                        fill=self.color, outline=""
                    )
            
            # Draw main particle
            canvas.create_oval(
                self.x - size, self.y - size,
                self.x + size, self.y + size,
                fill=self.color, outline=""
            )
        else:  # Confetti
            # Draw as rotating rectangle
            canvas.create_polygon(
                self.get_confetti_points(size),
                fill=self.color, outline=""
            )
    
    def get_confetti_points(self, size):
        """Get rotated rectangle points for confetti."""
        angle = math.radians(self.rotation)
        w, h = size * 2, size
        points = []
        for dx, dy in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            points.extend([self.x + rx, self.y + ry])
        return points


class Firework:
    """A firework that launches and explodes."""
    def __init__(self, canvas_width, canvas_height):
        self.x = random.randint(100, canvas_width - 100)
        self.y = canvas_height
        self.target_y = random.randint(100, canvas_height // 2)
        self.vy = random.uniform(-18, -12)
        self.color = self.random_bright_color()
        self.exploded = False
        self.particles = []
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
    
    def random_bright_color(self):
        """Generate a random bright color."""
        hue = random.random()
        saturation = random.uniform(0.7, 1.0)
        value = random.uniform(0.8, 1.0)
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    def update(self):
        """Update firework state."""
        if not self.exploded:
            self.y += self.vy
            self.vy += 0.3
            
            if self.vy >= 0 or self.y <= self.target_y:
                self.explode()
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        return not self.exploded or len(self.particles) > 0
    
    def explode(self):
        """Create explosion particles."""
        self.exploded = True
        num_particles = random.randint(50, 100)
        
        # Create explosion pattern
        pattern = random.choice(['circle', 'star', 'heart', 'double'])
        
        for i in range(num_particles):
            if pattern == 'circle':
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 8)
            elif pattern == 'star':
                angle = (i / num_particles) * 2 * math.pi
                speed = 6 if i % 5 == 0 else 3
            elif pattern == 'heart':
                t = (i / num_particles) * 2 * math.pi
                speed = 5
                angle = t
            else:  # double
                angle = random.uniform(0, 2 * math.pi)
                speed = random.choice([3, 7])
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Use main color or slight variation
            if random.random() < 0.8:
                color = self.color
            else:
                color = self.random_bright_color()
            
            self.particles.append(Particle(self.x, self.y, color, vx, vy))
    
    def draw(self, canvas):
        """Draw firework and its particles."""
        if not self.exploded:
            # Draw launching rocket
            canvas.create_oval(
                self.x - 4, self.y - 4,
                self.x + 4, self.y + 4,
                fill=self.color, outline="white"
            )
            # Draw trail
            for i in range(5):
                ty = self.y + i * 8
                size = 3 - i * 0.5
                if size > 0:
                    canvas.create_oval(
                        self.x - size, ty - size,
                        self.x + size, ty + size,
                        fill=self.color, outline=""
                    )
        
        # Draw particles
        for particle in self.particles:
            particle.draw(canvas)


class NewYearCelebration:
    """Main celebration application."""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎆 Happy New Year 2026! 🎆")
        
        # Fullscreen
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='black')
        
        # Get screen dimensions
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg='#0a0a1a',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Celebration state
        self.fireworks = []
        self.confetti = []
        self.stars = self.create_stars(200)
        self.show_countdown = True
        self.celebration_started = False
        self.text_colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        self.color_index = 0
        self.animation_running = True
        self.glow_phase = 0
        
        # Bind escape key to exit
        self.window.bind('<Escape>', lambda e: self.quit())
        self.window.bind('<space>', lambda e: self.add_fireworks(5))
        self.window.bind('<Button-1>', self.click_firework)
        
        # Start animation
        self.animate()
        
    def create_stars(self, count):
        """Create background stars."""
        stars = []
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 2)
            size = random.uniform(0.5, 2)
            brightness = random.uniform(0.3, 1)
            twinkle_speed = random.uniform(0.02, 0.08)
            stars.append({
                'x': x, 'y': y, 'size': size,
                'brightness': brightness,
                'twinkle_speed': twinkle_speed,
                'phase': random.uniform(0, 2 * math.pi)
            })
        return stars
    
    def click_firework(self, event):
        """Launch firework at click position."""
        fw = Firework(self.width, self.height)
        fw.x = event.x
        fw.target_y = event.y
        fw.y = self.height
        self.fireworks.append(fw)
    
    def add_fireworks(self, count=1):
        """Add new fireworks."""
        for _ in range(count):
            self.fireworks.append(Firework(self.width, self.height))
    
    def add_confetti(self, count=50):
        """Add confetti particles."""
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                  '#DDA0DD', '#FFD700', '#FF69B4', '#00CED1', '#FF4500']
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(-50, 0)
            vx = random.uniform(-2, 2)
            vy = random.uniform(2, 5)
            color = random.choice(colors)
            p = Particle(x, y, color, vx, vy, "confetti")
            p.decay = random.uniform(0.003, 0.008)
            self.confetti.append(p)
    
    def draw_gradient_background(self):
        """Draw a beautiful gradient background."""
        colors = [
            (10, 10, 40),   # Dark blue
            (20, 10, 50),   # Purple tint
            (10, 20, 60),   # Midnight blue
            (5, 5, 30)      # Very dark
        ]
        
        num_bands = 20
        band_height = self.height // num_bands
        
        for i in range(num_bands):
            ratio = i / num_bands
            r = int(10 + ratio * 15)
            g = int(10 + ratio * 10)
            b = int(40 - ratio * 20)
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            y1 = i * band_height
            y2 = (i + 1) * band_height
            self.canvas.create_rectangle(0, y1, self.width, y2, fill=color, outline="")
    
    def draw_stars(self):
        """Draw twinkling stars."""
        for star in self.stars:
            star['phase'] += star['twinkle_speed']
            twinkle = (math.sin(star['phase']) + 1) / 2
            brightness = int(100 + twinkle * 155 * star['brightness'])
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
            
            size = star['size'] * (0.8 + twinkle * 0.4)
            x, y = star['x'], star['y']
            
            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=color, outline=""
            )
    
    def draw_main_text(self):
        """Draw the main celebration text with effects."""
        self.glow_phase += 0.05
        
        # Calculate center
        cx = self.width // 2
        cy = self.height // 2
        
        # Pulsing effect
        pulse = math.sin(self.glow_phase) * 0.1 + 1
        
        # Rainbow color cycling
        hue = (self.glow_phase / 10) % 1
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1)
        glow_color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        
        # Draw "HAPPY NEW YEAR" with glow
        main_text = "✨ HAPPY NEW YEAR ✨"
        year_text = "2026"
        
        # Glow effect (multiple layers)
        for i in range(5, 0, -1):
            alpha_hex = int(255 * (1 - i/6))
            glow_size = int(60 * pulse) + i * 3
            
            self.canvas.create_text(
                cx, cy - 80,
                text=main_text,
                font=("Arial", glow_size, "bold"),
                fill=glow_color
            )
        
        # Main text
        self.canvas.create_text(
            cx, cy - 80,
            text=main_text,
            font=("Arial", int(60 * pulse), "bold"),
            fill="white"
        )
        
        # Year with special effect
        year_colors = ['#FFD700', '#FFA500', '#FF6347', '#FFD700']
        color_idx = int(self.glow_phase * 2) % len(year_colors)
        
        # Year glow
        for i in range(8, 0, -1):
            year_size = int(150 * pulse) + i * 2
            self.canvas.create_text(
                cx, cy + 50,
                text=year_text,
                font=("Arial", year_size, "bold"),
                fill=year_colors[color_idx]
            )
        
        # Main year
        self.canvas.create_text(
            cx, cy + 50,
            text=year_text,
            font=("Arial", int(150 * pulse), "bold"),
            fill="white"
        )
        
        # Subtitle
        messages = [
            "🎊 Wishing you joy, peace, and prosperity! 🎊",
            "🌟 May all your dreams come true! 🌟",
            "🎉 Cheers to new beginnings! 🎉",
            "💫 Here's to an amazing year ahead! 💫"
        ]
        msg_idx = int(self.glow_phase / 3) % len(messages)
        
        self.canvas.create_text(
            cx, cy + 180,
            text=messages[msg_idx],
            font=("Arial", 24, "italic"),
            fill="#FFEAA7"
        )
        
        # Instructions
        self.canvas.create_text(
            cx, self.height - 50,
            text="🖱️ Click anywhere for fireworks  |  SPACE for burst  |  ESC to exit",
            font=("Arial", 14),
            fill="#888888"
        )
    
    def draw_countdown(self):
        """Draw countdown to New Year (if before midnight)."""
        # For demo purposes, we'll skip to celebration
        # In real use, this would countdown to actual New Year
        pass
    
    def animate(self):
        """Main animation loop."""
        if not self.animation_running:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw background
        self.draw_gradient_background()
        
        # Draw stars
        self.draw_stars()
        
        # Add random fireworks
        if random.random() < 0.03:  # 3% chance each frame
            self.add_fireworks(1)
        
        # Add confetti occasionally
        if random.random() < 0.05:
            self.add_confetti(10)
        
        # Update and draw fireworks
        self.fireworks = [fw for fw in self.fireworks if fw.update()]
        for fw in self.fireworks:
            fw.draw(self.canvas)
        
        # Update and draw confetti
        self.confetti = [c for c in self.confetti if c.update() and c.y < self.height]
        for confetti in self.confetti:
            confetti.draw(self.canvas)
        
        # Draw main text
        self.draw_main_text()
        
        # Continue animation
        self.window.after(16, self.animate)  # ~60 FPS
    
    def quit(self):
        """Exit the application."""
        self.animation_running = False
        self.window.destroy()
    
    def run(self):
        """Start the celebration!"""
        # Add initial fireworks
        self.add_fireworks(10)
        self.add_confetti(100)
        
        self.window.mainloop()


class CountdownWindow:
    """Optional: A countdown window before the celebration."""
    
    def __init__(self, target_time=None):
        self.window = tk.Tk()
        self.window.title("Countdown to 2026!")
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='#1a1a2e')
        
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        
        # Default to demo countdown (10 seconds)
        if target_time:
            self.target = target_time
        else:
            self.target = datetime.now() + timedelta(seconds=10)
        
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.window.bind('<Escape>', lambda e: self.skip())
        self.window.bind('<space>', lambda e: self.skip())
        
        self.update_countdown()
    
    def skip(self):
        """Skip to celebration."""
        self.window.destroy()
        celebration = NewYearCelebration()
        celebration.run()
    
    def update_countdown(self):
        """Update countdown display."""
        now = datetime.now()
        remaining = self.target - now
        
        if remaining.total_seconds() <= 0:
            self.window.destroy()
            celebration = NewYearCelebration()
            celebration.run()
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw countdown
        total_seconds = int(remaining.total_seconds())
        
        if total_seconds <= 10:
            # Big countdown for last 10 seconds
            text = str(total_seconds)
            size = 300
            color = '#FF6B6B' if total_seconds <= 3 else '#FFD700'
        else:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            size = 100
            color = '#4ECDC4'
        
        # Glow effect
        for i in range(5, 0, -1):
            self.canvas.create_text(
                self.width // 2, self.height // 2,
                text=text,
                font=("Arial", size + i * 5, "bold"),
                fill=color
            )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=text,
            font=("Arial", size, "bold"),
            fill='white'
        )
        
        # Title
        self.canvas.create_text(
            self.width // 2, 100,
            text="🎆 Countdown to 2026! 🎆",
            font=("Arial", 48, "bold"),
            fill='#FFD700'
        )
        
        # Instructions
        self.canvas.create_text(
            self.width // 2, self.height - 50,
            text="Press SPACE to skip countdown | ESC to exit",
            font=("Arial", 16),
            fill='#888888'
        )
        
        self.window.after(100, self.update_countdown)
    
    def run(self):
        self.window.mainloop()


def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🎆 HAPPY NEW YEAR 2026 CELEBRATION 🎆                    ║
    ║                                                               ║
    ║     Controls:                                                 ║
    ║     • Click anywhere to launch fireworks                      ║
    ║     • Press SPACE for firework burst                          ║
    ║     • Press ESC to exit                                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    choice = input("Start mode:\n[1] Direct Celebration\n[2] 10-Second Countdown\n\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        countdown = CountdownWindow()
        countdown.run()
    else:
        celebration = NewYearCelebration()
        celebration.run()


if __name__ == "__main__":
    main()