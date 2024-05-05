# couponcodes

Implements the Coupon Codes Algorithm from Dan Mclean:

- https://www.mclean.net.nz/cpan/couponcode/
- https://github.com/grantm/Algorithm-CouponCode?tab=readme-ov-file

CouponCodes are designed to be distributed in printed form and typed into a web form. Features of the codes that make them well suited to manual transcription:

- The codes are not case sensitive.
- Not all letters and numbers are used, so if a person enters the letter 'O' we can automatically correct it to the digit '0' (similarly for I ⇨ 1, S ⇨ 5, Z ⇨ 2).
- The 4th character of each part is a checkdigit, so client-side scripting can be used to highlight parts which have been mis-typed, before the code is even submitted to the application's back-end validation.
- The checkdigit algorithm takes into account the position of the part being keyed. So for example '1K7Q' might be valid in the first part but not in the second so if a user typed the parts in the wrong boxes then their error could be highlighted.
- The code generation algorithm avoids 'undesirable' codes. For example any code in which transposed characters happen to result in a valid checkdigit will be skipped. Any generated part which happens to spell an 'inappropriate' 4-letter word (e.g.: 'P00P') will also be skipped.
- Codes can be generated and validated on the server

## Meta

This python implementation is not written or endorsed by Dan Mclean.

PyPi page: https://pypi.org/project/cccodes/
Githup page: https://github.com/birlorg/couponcodes

Known bugs/shortcomings compared to upstream:

- Too lazy to rot13 the bad words, you have to live with them in the repo.
- You can not select your own plaintext, it will only generate new random codes.
- This code has been barely tested and not audited, security and fit for purpose is your problem.

All other shortcomings are bugs and you should file issues.
Patches to fix the known shortcomings welcome.

## Usage

```python
pip install cccodes

# Generate a code:
python3 -c "import cccodes;print(cccodes.generate())"
66WUX-FJ5XA-6WUBU

# validate a code:
python3 -c "import cccodes;print(cccodes.validate('66wUX-FJ5XA-6WUBU'))"
True

# invalid check digit in 1st part from above code.
python3 -c "import cccodes;print(cccodes.validate('66WU7-FJ5XA-6WUBU'))"
False

# if you are storing the codes that are generated, so you can prevent re-use or whatever:
python3 -c "import cccodes;print(cccodes.normalize('tI3P-SLMP-E0B5'))"
T13P-5LMP-E0B5
#FYI: don't worry, validate will call normalize() for you, so you don't have to.

```
