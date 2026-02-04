// Checkbox logic
const checkboxes = document.querySelectorAll('input[name="allergies"]');
const noneCheckbox = document.querySelector('input[value="None"]');

checkboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', () => {
    if (noneCheckbox.checked) {
      checkboxes.forEach(cb => {
        if (cb !== noneCheckbox) {
          cb.checked = false;
          cb.disabled = true;
        }
      });
    } else {
      checkboxes.forEach(cb => cb.disabled = false);
    }

    const otherChecked = Array.from(checkboxes).some(cb => cb.checked && cb !== noneCheckbox);
    noneCheckbox.disabled = otherChecked;
  });
});

// Allergy descriptions
const allergyDetails = {
  "Allergic rash risk": "May cause rashes or skin irritation upon exposure.",
  "Allergic reaction risk": "Can trigger immune responses such as swelling, itching, or difficulty breathing.",
  "Allergy risk(injection site)": "Injection site may become red, swollen, or irritated.",
  "Cephalosphorin allergy": "Avoid cephalosporins if you're allergic to penicillin; possible cross-reactivity.",
  "Liver toxicity and allergy risk": "Can affect liver function and cause allergic responses.",
  "NSAID allergy": "NSAIDs like ibuprofen may cause stomach issues, rashes, or severe allergic reactions.",
  "Penicillin allergy": "May lead to hives, swelling, and severe anaphylactic reactions.",
  "Stevens johnson syndrome": "Rare but serious disorder of skin and mucous membranes; can be fatal.",
  "Sulfa allergy": "Allergic reactions to sulfonamide drugs.",
  "Sulpha allergy with combination": "Reactions to combined sulpha-based medications.",
  "Tetracycline allergy": "Can cause photosensitivity, rashes, and stomach upset.",
  "Topical allergy risk": "Reactions like burning, itching or rash where the medicine is applied.",
  "None": "No allergies reported."
};

// Modal elements
const modal = document.getElementById('infoModal');
const modalTitle = document.getElementById('modalTitle');
const modalDesc = document.getElementById('modalDescription');
const closeModalBtn = document.getElementById('closeModal');

// Show modal with allergy info
function showInfo(allergyName, event) {
  if (event.target.tagName === "INPUT") return; // skip if clicked on checkbox

  const description = allergyDetails[allergyName] || "Information not available.";
  modalTitle.textContent = allergyName;
  modalDesc.textContent = description;
  modal.style.display = "flex"; // using flex for centering
}

// Close modal on X click
closeModalBtn.onclick = function () {
  modal.style.display = "none";
};

// Close modal on outside click
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// Form submission logic
const form = document.getElementById('findform');
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const selectedAllergies = Array.from(document.querySelectorAll('input[name="allergies"]:checked'))
    .map(cb => cb.value.toLowerCase());

  if (noneCheckbox.checked) selectedAllergies.length = 0;

  const medicineName = form.querySelector('input[name="medicine"]').value.trim().toLowerCase();

  if (!medicineName) {
    alert('Please enter a medicine name.');
    return;
  }

  const data = {
    medicine: medicineName,
    allergies: selectedAllergies
  };

  try {
    const response = await fetch('/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const result = await response.json();
    const resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;

  } catch (error) {
    alert('Error: ' + error.message);
  }
});