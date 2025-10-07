(function(){
	function getBasePath(){
		const link = document.querySelector('link[rel="stylesheet"]');
		if(!link) return './';
		return link.href.replace(/static\/styles\.css.*/, '');
	}
	async function fetchIndex(){
		if(window.__kbIndex) return window.__kbIndex;
		const basePath = getBasePath();
		const res = await fetch(basePath + 'index.json',{cache:'no-store'});
		if(!res.ok) return [];
		const data = await res.json();
		window.__kbIndex = data;
		return data;
	}
	function normalize(s){return (s||'').toLowerCase();}
	function includes(hay,needle){return normalize(hay).includes(normalize(needle));}
	async function init(){
		const input = document.getElementById('search-input');
		if(!input) return;
		const list = document.querySelector('.doc-list');
		const basePath = getBasePath();
		const index = await fetchIndex();
		const bySlug = new Map(index.documents.map(d=>[d.slug,d]));
		function render(docs){
			list.innerHTML = '';
			for(const doc of docs){
				const li = document.createElement('li');
				const a = document.createElement('a');
				a.href = basePath + 'docs/' + doc.slug + '.html';
				a.textContent = doc.title;
				const meta = document.createElement('span');
				meta.className = 'meta';
				meta.textContent = `${doc.pages} pages • ${doc.size_human}`;
				li.appendChild(a);
				li.appendChild(meta);
				list.appendChild(li);
			}
		}
		render(index.documents);
		input.addEventListener('input', ()=>{
			const q = input.value.trim();
			if(!q){render(index.documents);return;}
			const results = new Map();
			for(const doc of index.documents){
				if(includes(doc.title,q)) results.set(doc.slug, doc);
			}
			for(const chunk of index.chunks){
				if(includes(chunk.text,q)){
					const d = bySlug.get(chunk.slug);
					if(d) results.set(d.slug,d);
				}
			}
			render(Array.from(results.values()));
		});
	}
	document.addEventListener('DOMContentLoaded', init);
})();