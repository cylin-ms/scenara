#!/usr/bin/env python3
"""
Screenshot utility for Scenara project
Captures screenshots of web interfaces for verification and documentation
"""

import argparse
import asyncio
import sys
import os
from typing import Optional, Tuple
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: Playwright not installed. Screenshot functionality limited.", file=sys.stderr)

class ScreenshotCapture:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
    
    async def __aenter__(self):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright is required for screenshot capture")
        
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        # Create context
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Scenara Screenshot Bot 1.0'
        )
        
        # Create page
        self.page = await self.context.new_page()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def capture_screenshot(
        self, 
        url: str, 
        output_path: str, 
        width: int = 1920, 
        height: int = 1080,
        wait_time: int = 3,
        element_selector: Optional[str] = None
    ) -> str:
        """
        Capture screenshot of a web page
        
        Args:
            url: URL to capture
            output_path: Path to save screenshot
            width: Viewport width
            height: Viewport height
            wait_time: Seconds to wait before capture
            element_selector: CSS selector to capture specific element
            
        Returns:
            Path to saved screenshot
        """
        try:
            print(f"Capturing screenshot of: {url}", file=sys.stderr)
            
            # Set viewport
            await self.page.set_viewport_size({"width": width, "height": height})
            
            # Navigate to URL
            await self.page.goto(url, wait_until='networkidle')
            
            # Wait for page to load
            await asyncio.sleep(wait_time)
            
            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Capture screenshot
            if element_selector:
                # Capture specific element
                element = await self.page.query_selector(element_selector)
                if element:
                    await element.screenshot(path=output_path)
                else:
                    print(f"Warning: Element '{element_selector}' not found", file=sys.stderr)
                    await self.page.screenshot(path=output_path, full_page=True)
            else:
                # Capture full page
                await self.page.screenshot(path=output_path, full_page=True)
            
            print(f"Screenshot saved: {output_path}", file=sys.stderr)
            return output_path
        
        except Exception as e:
            print(f"Screenshot capture failed: {e}", file=sys.stderr)
            raise
    
    async def capture_meeting_interface_screenshots(self, base_url: str, output_dir: str) -> list:
        """
        Capture screenshots of Scenara meeting interfaces
        
        Args:
            base_url: Base URL of the application
            output_dir: Directory to save screenshots
            
        Returns:
            List of captured screenshot paths
        """
        screenshots = []
        
        # Define key interfaces to capture
        interfaces = [
            {
                "name": "data_explorer_main",
                "url": f"{base_url}",
                "description": "Main data explorer interface"
            },
            {
                "name": "meeting_classification",
                "url": f"{base_url}?view=classification",
                "description": "Meeting classification view"
            },
            {
                "name": "gutt_evaluation",
                "url": f"{base_url}?view=evaluation",
                "description": "GUTT evaluation interface"
            },
            {
                "name": "data_separation",
                "url": f"{base_url}?view=separation",
                "description": "Data separation view"
            }
        ]
        
        for interface in interfaces:
            try:
                output_path = os.path.join(output_dir, f"{interface['name']}.png")
                await self.capture_screenshot(interface['url'], output_path)
                screenshots.append({
                    "name": interface['name'],
                    "path": output_path,
                    "description": interface['description'],
                    "url": interface['url']
                })
            except Exception as e:
                print(f"Failed to capture {interface['name']}: {e}", file=sys.stderr)
        
        return screenshots

def take_screenshot_sync(url: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
    """
    Synchronous wrapper for screenshot capture
    
    Args:
        url: URL to capture
        output_path: Path to save screenshot
        width: Viewport width
        height: Viewport height
        
    Returns:
        Path to saved screenshot
    """
    async def _capture():
        async with ScreenshotCapture() as capture:
            return await capture.capture_screenshot(url, output_path, width, height)
    
    return asyncio.run(_capture())

async def main():
    parser = argparse.ArgumentParser(description="Screenshot capture for Scenara")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", default="screenshot.png", help="Output file path")
    parser.add_argument("--width", type=int, default=1920, help="Viewport width")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height")
    parser.add_argument("--wait", type=int, default=3, help="Wait time before capture")
    parser.add_argument("--element", help="CSS selector for specific element")
    parser.add_argument("--meeting-interfaces", help="Capture all meeting interfaces from base URL")
    parser.add_argument("--output-dir", default="screenshots", help="Output directory")
    
    args = parser.parse_args()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("Error: Playwright not installed. Install with: pip install playwright", file=sys.stderr)
        print("Then run: playwright install chromium", file=sys.stderr)
        sys.exit(1)
    
    try:
        async with ScreenshotCapture() as capture:
            if args.meeting_interfaces:
                screenshots = await capture.capture_meeting_interface_screenshots(
                    args.url, args.output_dir
                )
                print(f"Captured {len(screenshots)} interface screenshots:")
                for screenshot in screenshots:
                    print(f"  {screenshot['name']}: {screenshot['path']}")
            else:
                await capture.capture_screenshot(
                    args.url, 
                    args.output, 
                    args.width, 
                    args.height,
                    args.wait,
                    args.element
                )
                print(f"Screenshot saved: {args.output}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())