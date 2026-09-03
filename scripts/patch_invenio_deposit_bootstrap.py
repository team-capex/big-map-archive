from pathlib import Path
import invenio_rdm_records

package_dir = Path(invenio_rdm_records.__file__).resolve().parent

path = (
    package_dir
    / "assets"
    / "semantic-ui"
    / "js"
    / "invenio_rdm_records"
    / "src"
    / "deposit"
    / "api"
    / "DepositBootstrap.js"
)

text = path.read_text()

old_import = """  submitReview,
} from "../state/actions";"""

new_import = """  submitReview as submitReviewAction,
} from "../state/actions";"""

old_dispatch = """  submitReview: (values, { reviewComment, directPublish }) =>
    dispatch(submitReview(values, { reviewComment, directPublish })),"""

new_dispatch = """  submitReview: (values, { reviewComment, directPublish }) =>
    dispatch(submitReviewAction(values, { reviewComment, directPublish })),"""

if new_import in text and new_dispatch in text:
    print(f"Patch already applied: {path}")
else:
    if old_import not in text:
        raise RuntimeError(
            "Expected submitReview import not found. "
            "invenio-rdm-records may have changed; inspect before deploying."
        )

    if old_dispatch not in text:
        raise RuntimeError(
            "Expected submitReview mapDispatchToProps code not found. "
            "invenio-rdm-records may have changed; inspect before deploying."
        )

    text = text.replace(old_import, new_import, 1)
    text = text.replace(old_dispatch, new_dispatch, 1)

    path.write_text(text)
    print(f"Patched: {path}")
