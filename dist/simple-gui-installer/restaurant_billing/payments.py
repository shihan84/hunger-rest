from pathlib import Path
from typing import Optional
import qrcode
from PIL import Image, ImageTk

from .config import CONFIG


def generate_upi_qr(payee_vpa: str, payee_name: str, amount: Optional[float] = None, note: Optional[str] = None, out_path: Optional[Path] = None) -> Path:
	params = [f"upi://pay?pa={payee_vpa}", f"pn={payee_name}"]
	if amount is not None:
		params.append(f"am={amount:.2f}")
	if note:
		params.append(f"tn={note}")
	data = "&".join(params)
	img = qrcode.make(data)
	if out_path is None:
		out_path = CONFIG.assets_path / "upi_qr.png"
	out_path.parent.mkdir(parents=True, exist_ok=True)
	img.save(out_path)
	return out_path


def tk_image_from_path(path: Path, size: int = 220) -> ImageTk.PhotoImage:
	img = Image.open(path).resize((size, size))
	return ImageTk.PhotoImage(img)
