from bardapi import Bard

token = 'cQg17qXW7dpFaOcVA3tIwAs_lu0W4ipB-KTVk307IuGkVT8hDb8IwxATIHGdo7-5RUx4yg.'
bard = Bard(token=token)

print(bard.get_answer("Explain Quantum Computers in 50 words"))