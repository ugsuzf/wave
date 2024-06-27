# Lesson 5: User interaction
# # Let's add some interactivity
# So far, we have only seen something called [Wave Script](https://wave.h2o.ai/docs/scripts/).
# These are simple python scripts (as the name suggests) and are meant for dashboards that only display data,
# but do not allow user interactions like button clicks for example. If you would like your users to be able
# to control the app via buttons, dropdowns etc. and capture these interactions, you will need to reach out
# for something called [Wave App](https://wave.h2o.ai/docs/apps).
# ## Basic app scaffolding
# * Necessary imports.
# * A single entrypoint async function with @app annotation where route, that the app listens on, is specified.
# 
# The entrypoint (serve) function provides a single parameter called `q` that acts allows you to control
# the whole app by handling interactions, registering cards etc. Note that this function is called every time a user
# interaction happens so that you can handle it accordingly.
# ## Simple example
# Let's render a markdown card together with a text input and button. Once you fill the text input and click
# the submit button, the content of the markdown card should be updated.
# ## Handling interactivity
# As we discussed previously, Wave gives you a "q" object. This object includes all the component values
# (for textbox, button, checkbox etc.) that has changed compared to the last time the serve function was called.
# These values are stored in a read-only dictionary "q.args" with key being the `name` attribute of the given
# component. For example button, with name "btn1" will have data stored in "q.args.btn1".
#  
# See [docs](https://wave.h2o.ai/docs/arguments) for more info.
# ## Your task
# Try to add another textbox component that would work the same as Content textbox, but for card title.
# ---
# ---
from h2o_wave import main, app, Q, ui
import asyncio

branch_coverage = {
    "if_submit": False,  # if submit branch
    "else_not_submit": False  # else not submit branch
}

@app('/demo')
async def serve(q: Q):
    q.page['hello'] = ui.markdown_card(box='1 1 3 1', title='Markdown card', content='Hello World!')
    q.page['form'] = ui.form_card(box='1 2 3 3', items=[
        ui.textbox(name='content', label='Content'),
        ui.button(name='submit', label='Submit'),
    ])

    # Handle the button click.
    if q.args.submit:
        # Update existing card content.
        q.page['hello'].content = q.args.content
        branch_coverage["if_submit"] = True # Coverage for form submission
    else:
        branch_coverage["else_not_submit"] = True   # Coverage for form not submitted

    await q.page.save()

def print_coverage():
    total_branches = len(branch_coverage)
    hit_branches = sum(branch_coverage.values())
    coverage_percentage = (hit_branches / total_branches) * 100
    for branch, hit in branch_coverage.items():
        print(f"{branch} was {'hit' if hit else 'not hit'}")
    print(f"Branch coverage: {coverage_percentage:.2f}%")

# Mocking classes for testing
class MockArgs:
    def __init__(self, submit, content=''):
        self.submit = submit
        self.content = content

class MockPage:
    def __init__(self):
        self.cards = {}

    def __setitem__(self, key, value):
        self.cards[key] = value

    def __getitem__(self, key):
        return self.cards[key]

    async def save(self):
        pass

class MockQ:
    def __init__(self, submit):
        self.page = MockPage()
        self.args = MockArgs(submit=submit)

async def test_with_submit():
    q = MockQ(submit=True)
    await serve(q)
    print("After test with submit:")
    print_coverage()

async def test_without_submit():
    q = MockQ(submit=False)
    await serve(q)
    print("After test without submit:")
    print_coverage()

async def run_tests():
    await test_with_submit()
    await test_without_submit()

asyncio.run(run_tests())