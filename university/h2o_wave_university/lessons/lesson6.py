# Lesson 6: User interaction II
# # Triggering components
# Clicking the submit button is fine, but there can be cases, when you may want to have the data
# submitted without a button click. Typical scenario can be a searchbox.
# 
# That's the purpose of "trigger" attribute - submit data after user stops typing or picks
# a dropdown option for example.
# 
# Notice that the example provided is a bit clunky - the text you type disappears after it's submitted.
# We will demystify and fix this behavior later on (in [lesson10](#lesson10)) so no worries. For
# simplicity sake, the example is good enough as is currently.
# ## Your task
# There is not much to play around with here so give yourself a pat on shoulder for making it this far!
# ---

from h2o_wave import main, app, Q, ui
import asyncio
from h2o_wave.core import Expando

# Mocking a minimal Site object
class MockSite:
    def __getitem__(self, item):
        return Expando()

class MockPage:
    def __init__(self):
        self.cards = {}

    def __getitem__(self, item):
        return self.cards[item]

    def __setitem__(self, key, value):
        self.cards[key] = value

    async def save(self):
        pass

branch_coverage = {
    "if_q_args_content": False,  # if branch
    "else_q_args_content": False  # else branch (implicitly no action)
}

@app('/demo')
async def serve(q: Q):
    q.page['hello'] = ui.markdown_card(box='1 1 3 1', title='Markdown card', content='Hello World!')
    q.page['form'] = ui.form_card(box='1 2 3 2', items=[
        ui.textbox(name='content', label='Content', trigger=True),
    ])

    # Handle the button click.
    if q.args.content:
        # Update existing card content.
        q.page['hello'].content = q.args.content
        branch_coverage["if_q_args_content"] = True
    else:
        branch_coverage["else_q_args_content"] = True

    await q.page.save()

def print_coverage():
    total_branches = len(branch_coverage)
    hit_branches = sum(branch_coverage.values())
    coverage_percentage = (hit_branches / total_branches) * 100
    for branch, hit in branch_coverage.items():
        print(f"{branch} was {'hit' if hit else 'not hit'}")
    print(f"Branch coverage: {coverage_percentage:.2f}%")

async def test_serve_with_content():
    auth = Expando()
    auth.subject = 'test_user'

    args = Expando()
    args.content = 'New Content'

    q = Q(
        site=MockSite(),
        mode='',
        auth=auth,
        client_id='test_client',
        route='/',
        app_state=Expando(),
        user_state=Expando(),
        client_state=Expando(),
        args=args,
        events=Expando(),
        headers={}
    )
    q.page = MockPage()  # Mocking q.page
    await serve(q)
    print("After test with content:")
    print_coverage()

async def test_serve_without_content():
    auth = Expando()
    auth.subject = 'test_user'

    args = Expando()
    args.content = ''

    q = Q(
        site=MockSite(),
        mode='',
        auth=auth,
        client_id='test_client',
        route='/',
        app_state=Expando(),
        user_state=Expando(),
        client_state=Expando(),
        args=args,
        events=Expando(),
        headers={}
    )
    q.page = MockPage()  # Mocking q.page
    await serve(q)
    print("After test without content:")
    print_coverage()

async def run_tests():
    await test_serve_with_content()
    await test_serve_without_content()

if __name__ == '__main__':
    asyncio.run(run_tests())
