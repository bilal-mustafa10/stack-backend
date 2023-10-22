from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask import jsonify
from langchain.llms import AI21, OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# CORS(app, resources={r"/": {"origins": ""}})


@app.route('/')
def index():
    return jsonify({"message": "Hello"}), 200


# PromptTemplate.from_template(prompt_template)

@app.route('/generate_smart_contract', methods=['POST'])
def generate_smart_contract():
    data = request.get_json()
    contract_type = data['type']
    usecase = data['description']
    contract_parties = data['parties']
    contract_conditions = data['conditions']
    contract_payments = data['payments']
    contract_completions = data['completions']


    prompt_template = """
    Dear LLM,
    You are an expert in creating smart contracts. Your knowledge and understanding of blockchain technology, particularly Stacks, is unparalleled. I am in need of your expertise to create a smart contract.
    The contract should be written in Clarity and it should be compatible with the latest version of the Stacks 2.0 blockchain.
    Please ensure that the contract is secure and follows best practices for Clarity development. I trust your judgment in creating a contract that is efficient, secure, and easy to interact with.
    Generate accurate smart contract is for the following application {usecase} and dont stop untill you finish generating the complete contract and at the end say it is the END
    
    An example of a smart contract is given below:
    
    ;; An on-chain counter that stores a count for each individual
    
    ;; Define a map data structure
    (define-map counters principal uint)
    
    ;; Function to retrieve the count for a given individual
    (define-read-only (get-count (who principal))
        (default-to u0 (map-get? counters who))
    )
    
    ;; Function to increment the count for the caller
    (define-public (count-up)
        (ok (map-set counters tx-sender (+ (get-count tx-sender) u1)))
    )
    
    Another example of a smart contract is given below:
    ;; This contract implements the SIP-010 community-standard Fungible Token trait.
    (impl-trait 'SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE.sip-010-trait-ft-standard.sip-010-trait)

    ;; Define the FT, with no maximum supply
    (define-fungible-token clarity-coin)

    ;; Define errors
    (define-constant ERR_OWNER_ONLY (err u100))
    (define-constant ERR_NOT_TOKEN_OWNER (err u101))

    ;; Define constants for contract
    (define-constant CONTRACT_OWNER tx-sender)
    (define-constant TOKEN_URI u"https://hiro.so") ;; utf-8 string with token metadata host
    (define-constant TOKEN_NAME "Clarity Coin")
    (define-constant TOKEN_SYMBOL "CC")
    (define-constant TOKEN_DECIMALS u6) ;; 6 units displayed past decimal, e.g. 1.000_000 = 1 token


    ;; SIP-010 function: Get the token balance of a specified principal
    (define-read-only (get-balance (who principal))
        (ok (ft-get-balance clarity-coin who))
    )

    ;; SIP-010 function: Returns the total supply of fungible token
    (define-read-only (get-total-supply)
        (ok (ft-get-supply clarity-coin))
    )

    ;; SIP-010 function: Returns the human-readable token name
    (define-read-only (get-name)
        (ok TOKEN_NAME)
    )

    ;; SIP-010 function: Returns the symbol or "ticker" for this token
    (define-read-only (get-symbol)
        (ok TOKEN_SYMBOL)
    )

    ;; SIP-010 function: Returns number of decimals to display
    (define-read-only (get-decimals)
        (ok TOKEN_DECIMALS)
    )

    ;; SIP-010 function: Returns the URI containing token metadata
    (define-read-only (get-token-uri)
        (ok (some TOKEN_URI))
    )

    ;; Mint new tokens and send them to a recipient.
    ;; Only the contract deployer can perform this operation.
    (define-public (mint (amount uint) (recipient principal))
        (begin
            (asserts! (is-eq tx-sender CONTRACT_OWNER) ERR_OWNER_ONLY)
            (ft-mint? clarity-coin amount recipient)
        )
    )

    ;; SIP-010 function: Transfers tokens to a recipient
    ;; Sender must be the same as the caller to prevent principals from transferring tokens they do not own.
    (define-public (transfer
        (amount uint)
        (sender principal)
        (recipient principal)
        (memo (optional (buff 34)))
    )
    (begin
        ;; #[filter(amount, recipient)]
        (asserts! (is-eq tx-sender sender) ERR_NOT_TOKEN_OWNER)
        (try! (ft-transfer? clarity-coin amount sender recipient))
        (match memo to-print (print to-print) 0x)
        (ok true)
    )
    )
    """

    # prompt_template = """
    # Dear LLM,
    #
    # I hope this message finds you well. Your expertise in creating smart contracts has come highly recommended, and I am particularly impressed by your deep understanding of blockchain technology, specifically in the Stacks ecosystem.
    #
    # I am reaching out to seek your assistance in crafting a smart contract that adheres to best practices in Clarity language and is compatible with the latest version of Stacks 2.0 blockchain.
    #
    # Contract Requirements:
    #
    # - **Type**: {contract_type}
    # - **Description**: {contract_description}
    # - **Parties Involved**: {contract_parties}
    # - **Conditions**: {contract_conditions}
    # - **Payment Details**: {contract_payments}
    # - **Milestones and Completions**: {contract_completions}
    #
    # I place great trust in your judgment to develop a contract that is not only secure but also efficient and user-friendly. Could you please ensure that the smart contract satisfies the above requirements?
    #
    # Your task is to generate a smart contract for the specific application: {contract_description}. Kindly proceed with the development and inform me when the contract is complete by indicating 'END'.
    #
    # Thank you for your attention to this matter. I look forward to your positive response.
    # """

    prompt = PromptTemplate(template=prompt_template, input_variables=["usecase"])
    llm = AI21(model="j2-ultra")
    # llm = OpenAIChat(temperature=0.2,model='gpt-3.5-turbo-16k')
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # prompt=PromptTemplate.from_template(prompt_template)
    llm_out = llm_chain(usecase)
    print(llm_out)
    return jsonify({"LLM Says": llm_out}), 200


# find vulnerabilities in smart contract
@app.route('/find_vulnerabilities', methods=['POST'])
def find_vulnerabilities():
    data = request.get_json()
    usecase = data['usecase']
    smart_contract = data['smart_contract']
    prompt_template = """
    Dear LLM,
    You are an expert in finding vulnerabilities in smart contracts. Your knowledge and understanding of blockchain technology, particularly Stacks, is unparalleled. I am in need of your expertise to find vulnerabilities in a smart contract.
    The contract should be written in Clarity and it should be compatible with the latest version of the Stacks 2.0 blockchain.
    Please ensure that the contract is secure and follows best practices for Clarity development. I trust your judgment in finding vulnerabilities in the contract.
    Find vulnerabilities in smart contract is for the following application {usecase} and dont stop untill you finish finding all the vulnerabilities and at the end say it is the END
    Here is the smart contract: {smart_contract}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["usecase", "smart_contract"])
    llm = AI21(model="j2-ultra")
    # llm = OpenAIChat(temperature=0.2,model='gpt-3.5-turbo-16k')prompt = PromptTemplate(data['prompt'])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # prompt=PromptTemplate.from_template(prompt_template)
    llm_out = llm_chain(usecase, smart_contract)
    inputs = {
        "usecase": usecase,
        "smart_contract": smart_contract
    }
    llm_out = llm_chain(inputs)
    return jsonify({"LLM Says": llm_out}), 200


# Talk to existing smart contract
@app.route('/talk_to_user_about_smart_contract', methods=['POST'])
# We talk  to user and AI has to make changes accordingly
def talk_to_user_about_smart_contract():
    data = request.get_json()
    usecase = data['usecase']
    smart_contract = data['smart_contract']
    prompt_template = """
    Dear LLM,
    You are an expert in talking to users about smart contracts. Your knowledge and understanding of blockchain technology, particularly Stacks, is unparalleled. I am in need of your expertise to talk to users about a smart contract.
    The contract should be written in Clarity and it should be compatible with the latest version of the Stacks 2.0 blockchain.
    Please ensure that the contract is secure and follows best practices for Clarity development. I trust your judgment in talking to users about the contract.
    Talk to user about smart contract is for the following application {usecase} and dont stop untill you finish talking to user and at the end say it is the END
    Here is the smart contract: {smart_contract} and make any changes user wants you to do and return the altered full contract.
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["usecase", "smart_contract"])
    llm = AI21(model="j2-ultra")
    # llm = OpenAIChat(temperature=0.2,model='gpt-3.5-turbo-16k')prompt = PromptTemplate(data['prompt'])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # prompt=PromptTemplate.from_template(prompt_template)
    llm_out = llm_chain(usecase, smart_contract)
    inputs = {
        "usecase": usecase,
        "smart_contract": smart_contract
    }
    llm_out = llm_chain(inputs)
    return jsonify({"LLM Says": llm_out}), 200


if __name__ == '_main_':
    app.run(debug=True)
