# Lesson 10: State II
# # Create once, update afterwards
# Remember how the input we typed in [lesson5](#lesson5) disappeared after submit?
# It was because we recreated the markdown card by assigning q.page['form'] a new card reference
# after every submit instead of creating it just once.
# 
# For creating it just once, we would need to identify first render somehow. Luckily for us,
# it's very straightforward in Wave - just set a boolean client-scope variable initialized (or any other name)
# to True after the serve function runs for the first time.
# 
# The following example uses q.client for storage since we want to create the card once per every tab. However,
# the very same technique can be used with q.app if you want to make some action once per whole app lifecycle
# like training a small model or q.user to make something once per user session.
# 
# ## Simple example
# This app will do the exact same thing as [lesson5](#lesson5) did, but this time, the textbox input
# will keep the value.
# ## Your task
# Try to fix the example from [lesson6](#lesson6).
# ---

from h2o_wave import main, app, Q, ui
import asyncio

branch_coverage = {
    "if_client_not_initialized": False,  # if not q.client.initialized branch
    "if_submit": False,  # if q.args.submit branch
    "else_initialized": False,  # else initialized branch
    "else_not_submit":False # else not submit branch
}

@app('/demo')
async def serve(q: Q):
    if not q.client.initialized:
        branch_coverage["if_client_not_initialized"] = True  # Coverage for client not initialized
        # Create cards only once per browser.
        q.page['hello'] = ui.markdown_card(box='1 1 3 1', title='Markdown card', content='Hello World!')
        q.page['form'] = ui.form_card(box='1 2 3 3', items=[
            ui.textbox(name='content', label='Content'),
            ui.button(name='submit', label='Submit'),
        ])
        q.client.initialized = True
    else:
        branch_coverage["else_initialized"] = True  # Coverage for client initialized

    # Handle the button click.
    if q.args.submit:
        branch_coverage["if_submit"] = True  # Coverage for form submission
        # Update existing card content.
        q.page['hello'].content = q.args.content
    else:
        branch_coverage["else_not_submit"] = True  # Coverage for form not submitted

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
    def __init__(self, submit=False):
        self.submit = submit
        self.content = ""

class MockPage:
    def __init__(self):
        self.cards = {}

    def __setitem__(self, key, value):
        self.cards[key] = value

    def __getitem__(self, key):
        return self.cards[key]

    async def save(self):
        pass

class MockClient:
    def __init__(self, initialized=False):
        self.initialized = initialized

class MockQ:
    def __init__(self, submit=False, initialized=False):
        self.page = MockPage()
        self.args = MockArgs(submit=submit)
        self.client = MockClient(initialized=initialized)
        if initialized:
            self.page['hello'] = ui.markdown_card(box='1 1 3 1', title='Markdown card', content='Hello World!')

async def test_with_initialization():
    q = MockQ(initialized=True)
    await serve(q)
    print("After test with initialization:")
    print_coverage()

async def test_without_initialization():
    q = MockQ(initialized=False)
    await serve(q)
    print("After test without initialization:")
    print_coverage()

async def test_with_submit():
    q = MockQ(submit=True)
    await serve(q)
    print("After test with submit true:")
    print_coverage()

async def run_tests():
    await test_with_initialization()
    await test_without_initialization()
    await test_with_submit()

asyncio.run(run_tests())
